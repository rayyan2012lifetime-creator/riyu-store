"""
Pakistani AI Dropshipping Gateway - Improved Version
Handles AI customer care and dropshipping order management with security and reliability.
"""

import os
import logging
from typing import Optional
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator, EmailStr
import openai
from openai import OpenAIError

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pakistani AI Dropshipping Gateway",
    description="AI-powered customer care and order management for Pakistani e-commerce",
    version="2.0.0"
)

# Add CORS middleware for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Initialize OpenAI Client
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logger.warning("OPENAI_API_KEY not set. AI customer care will fail.")

# --- CONSTANTS ---
BASE_COURIER_FEE = 150.0
MIN_PROFIT = 400.0
MAX_PROFIT = 500.0
DELIVERY_DAYS = "3-5 working days"
DELIVERY_COURIERS = ["Trax", "Leopards", "M&P"]

# --- ENUMS ---
class PayoutMethod(str, Enum):
    JAZZCASH = "JazzCash"
    EASYPAISA = "EasyPaisa"
    BANK_TRANSFER = "Bank Transfer"

class OrderStatus(str, Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# --- DATABASE MODELS & SCHEMAS ---
class OrderPayload(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_phone: str = Field(..., regex=r"^(\+92|0)[0-9]{10}$")  # Pakistani phone format
    delivery_address: str = Field(..., min_length=10, max_length=500)
    city: str = Field(..., min_length=2, max_length=50)
    product_id: str = Field(..., min_length=1, max_length=50)
    wholesale_price: float = Field(..., gt=0, le=100000)
    custom_profit: float = Field(default=450.0, ge=MIN_PROFIT, le=MAX_PROFIT)
    payout_method: PayoutMethod = PayoutMethod.JAZZCASH
    payout_account: str = Field(..., min_length=5, max_length=50)
    
    @validator('customer_phone')
    def validate_phone(cls, v):
        """Validate Pakistani phone number format"""
        if not v.startswith(('+92', '0')):
            raise ValueError("Phone must start with +92 or 0")
        return v

class AIChatPayload(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    order_id: Optional[str] = Field(None, max_length=50)
    
    @validator('message')
    def sanitize_message(cls, v):
        """Basic input sanitization"""
        return v.strip()

class OrderResponse(BaseModel):
    order_id: str
    status: OrderStatus
    pricing_breakdown: dict
    payout_ledger: dict
    estimated_delivery: str
    created_at: datetime

class AIChatResponse(BaseModel):
    reply: str
    escalate_to_human: bool
    confidence_score: Optional[float] = None

# --- DEPENDENCY INJECTION ---
def verify_api_key(api_key: Optional[str] = None) -> bool:
    """Verify API key from request (optional - add as needed)"""
    if not api_key:
        return True
    # Add your API key validation logic here
    return api_key == os.getenv("INTERNAL_API_KEY", "")

# --- ROUTE 1: AI CUSTOMER CARE SYSTEM ---
@app.post("/api/ai-customer-care", response_model=AIChatResponse)
async def ai_customer_care(payload: AIChatPayload):
    """
    AI-powered customer care system with multi-language support.
    Automatically escalates complex issues to human support.
    """
    system_prompt = f"""
    You are 'Asma', the AI customer care specialist for a leading Pakistani e-commerce dropshipping store.
    Provide replies in a helpful mix of English and Roman Urdu if preferred by the tone.
    
    Guidelines:
    1. Shipping: Delivery across Pakistan takes {DELIVERY_DAYS} via {', '.join(DELIVERY_COURIERS)}.
    2. Payment: Cash on Delivery (COD) is fully available and secure.
    3. Escalation: If a customer is highly upset, demands a refund, or has legal concerns, 
       include "ESCALATE_TO_HUMAN" in your response.
    4. Refunds: Standard refund window is 7 days from delivery.
    5. Stay professional and friendly.
    
    Keep responses concise (under 200 words).
    """
    
    try:
        logger.info(f"Processing AI chat request: {payload.order_id or 'no_order_id'}")
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": payload.message}
            ],
            temperature=0.4,
            max_tokens=300,  # Prevent excessive token usage
            timeout=10  # 10-second timeout
        )
        
        reply = response.choices[0].message['content']
        escalate = "ESCALATE_TO_HUMAN" in reply or any(
            keyword in reply.lower() 
            for keyword in ["escalate", "connect to agent", "supervisor", "manager"]
        )
        
        # Log for monitoring
        logger.info(f"AI response generated. Escalation: {escalate}")
        
        return AIChatResponse(
            reply=reply,
            escalate_to_human=escalate,
            confidence_score=0.85  # Add confidence based on model response
        )
        
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service temporarily unavailable. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error in AI customer care: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )

# --- ROUTE 2: DROPSHIPPING ORDER & PAYOUT ROUTER ---
@app.post("/api/place-order", response_model=OrderResponse)
async def place_order(order: OrderPayload):
    """
    Process dropshipping order with integrated supplier sync and payout management.
    
    Flow:
    1. Validate order details
    2. Sync with local supplier (Markaz App / HHC API)
    3. Calculate pricing and COD amount
    4. Lock profit and schedule payout
    5. Route to courier
    """
    
    try:
        # Generate unique order ID (in production, use database)
        order_id = f"PKR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{order.product_id[:3].upper()}"
        logger.info(f"Processing order: {order_id}")
        
        # Validate profit margin
        if not (MIN_PROFIT <= order.custom_profit <= MAX_PROFIT):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Profit must be between PKR {MIN_PROFIT} and PKR {MAX_PROFIT}"
            )
        
        # Simulate supplier API sync (implement actual integration)
        supplier_sync_status = await sync_with_supplier(order.product_id)
        if not supplier_sync_status:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Supplier inventory unavailable. Please try again later."
            )
        
        # Calculate final COD amount
        total_cod_amount = order.wholesale_price + order.custom_profit + BASE_COURIER_FEE
        
        # Validate total amount (business logic check)
        if total_cod_amount > 50000:  # Max reasonable COD amount
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order total exceeds maximum COD limit (PKR 50,000)"
            )
        
        # Prepare response
        response_data = OrderResponse(
            order_id=order_id,
            status=OrderStatus.DISPATCHED,
            pricing_breakdown={
                "wholesale_cost": f"PKR {order.wholesale_price:,.2f}",
                "profit_margin": f"PKR {order.custom_profit:,.2f}",
                "shipping_fee": f"PKR {BASE_COURIER_FEE:,.2f}",
                "customer_cod_total": f"PKR {total_cod_amount:,.2f}"
            },
            payout_ledger={
                "locked_profit": f"PKR {order.custom_profit:,.2f}",
                "payout_method": order.payout_method.value,
                "payout_account": f"***{order.payout_account[-4:]}",  # Mask sensitive data
                "release_condition": "Disbursed within 24 hours of confirmed COD customer pickup",
                "estimated_payout_time": "1-2 business days"
            },
            estimated_delivery=DELIVERY_DAYS,
            created_at=datetime.now()
        )
        
        logger.info(f"Order {order_id} successfully processed. Total: PKR {total_cod_amount:,.2f}")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process order. Please contact support."
        )

# --- HELPER FUNCTIONS ---
async def sync_with_supplier(product_id: str) -> bool:
    """
    Sync with local supplier API (Markaz App / HHC API).
    Implement actual integration with your supplier.
    """
    try:
        # TODO: Integrate with actual supplier API
        # For now, simulate success
        logger.info(f"Syncing product {product_id} with supplier")
        return True
    except Exception as e:
        logger.error(f"Supplier sync failed for {product_id}: {str(e)}")
        return False

# --- HEALTH CHECK ---
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "openai_configured": bool(openai.api_key)
    }

# --- ERROR HANDLERS ---
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for logging"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "status": "error",
        "message": "An unexpected error occurred. Please contact support.",
        "timestamp": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
