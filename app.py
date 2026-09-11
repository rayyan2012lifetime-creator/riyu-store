"""
Pakistani AI Dropshipping Gateway - Daraz-Style E-commerce App
Modern e-commerce interface with product catalog, cart, checkout, and AI support.
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional, List
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Riyu Store - Pakistani Dropshipping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DARAZ-STYLE CSS ---
st.markdown("""
    <style>
    /* Daraz Color Scheme - Red/Yellow */
    :root {
        --daraz-red: #EE4D2D;
        --daraz-yellow: #FFE812;
        --daraz-dark: #232F3E;
        --daraz-light: #F5F5F5;
    }
    
    * {
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background-color: #F5F5F5;
    }
    
    /* Header Navigation */
    .header-nav {
        background: linear-gradient(90deg, #EE4D2D 0%, #FF6B35 100%);
        padding: 15px 30px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 0;
        margin: -60px -60px 30px -60px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .header-nav h1 {
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }
    
    /* Search Bar */
    .search-container {
        width: 100%;
        margin: 20px 0;
    }
    
    .search-box {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #EE4D2D;
        font-size: 16px;
    }
    
    /* Product Grid */
    .products-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .product-card {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .product-card:hover {
        box-shadow: 0 4px 12px rgba(238, 77, 45, 0.15);
        transform: translateY(-2px);
    }
    
    .product-image {
        width: 100%;
        height: 200px;
        background: #F5F5F5;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
    }
    
    .product-info {
        padding: 15px;
    }
    
    .product-name {
        font-size: 14px;
        font-weight: bold;
        color: #232F3E;
        margin-bottom: 8px;
        min-height: 35px;
    }
    
    .product-price {
        font-size: 20px;
        color: #EE4D2D;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .product-rating {
        font-size: 12px;
        color: #F59E0B;
        margin-bottom: 10px;
    }
    
    .product-button {
        width: 100%;
        padding: 10px;
        background: #EE4D2D;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .product-button:hover {
        background: #d63317;
    }
    
    /* Cart Sidebar */
    .cart-sidebar {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    
    .cart-header {
        font-size: 18px;
        font-weight: bold;
        color: #232F3E;
        margin-bottom: 15px;
        border-bottom: 2px solid #EE4D2D;
        padding-bottom: 10px;
    }
    
    .cart-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #F5F5F5;
        font-size: 13px;
    }
    
    .cart-total {
        font-size: 18px;
        font-weight: bold;
        color: #EE4D2D;
        margin: 15px 0;
        padding: 15px 0;
        border-top: 2px solid #EE4D2D;
    }
    
    /* Checkout Button */
    .checkout-btn {
        width: 100%;
        padding: 12px;
        background: linear-gradient(90deg, #EE4D2D 0%, #FF6B35 100%);
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
    }
    
    .checkout-btn:hover {
        opacity: 0.9;
    }
    
    /* Badges */
    .badge-flash {
        background: #FFE812;
        color: #232F3E;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    
    .badge-free-shipping {
        background: #10B981;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    
    /* Chat Widget */
    .chat-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        z-index: 999;
    }
    
    .chat-header {
        background: #EE4D2D;
        color: white;
        padding: 15px;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
    }
    
    .chat-messages {
        height: 300px;
        overflow-y: auto;
        padding: 15px;
    }
    
    .chat-input {
        padding: 10px;
        border-top: 1px solid #F5F5F5;
    }
    
    /* Tabs */
    .tab-container {
        display: flex;
        gap: 20px;
        margin: 20px 0;
        border-bottom: 2px solid #F5F5F5;
    }
    
    .tab-item {
        padding: 15px 20px;
        cursor: pointer;
        border-bottom: 3px solid transparent;
        font-weight: bold;
        color: #666;
        transition: all 0.3s;
    }
    
    .tab-item.active {
        color: #EE4D2D;
        border-bottom-color: #EE4D2D;
    }
    
    .tab-item:hover {
        color: #EE4D2D;
    }
    
    /* Promo Banner */
    .promo-banner {
        background: linear-gradient(90deg, #EE4D2D 0%, #FFE812 100%);
        padding: 20px;
        border-radius: 8px;
        color: white;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Checkout Form */
    .checkout-form {
        background: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    
    .form-section {
        margin-bottom: 25px;
        padding-bottom: 25px;
        border-bottom: 1px solid #F5F5F5;
    }
    
    .form-section h3 {
        color: #232F3E;
        margin-bottom: 15px;
        font-size: 18px;
    }
    
    .success-message {
        background: #D1FAE5;
        border-left: 4px solid #10B981;
        color: #065F46;
        padding: 15px;
        border-radius: 4px;
        margin: 20px 0;
    }
    
    .rating-stars {
        color: #FCD34D;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'products' not in st.session_state:
    st.session_state.products = [
        {"id": "PROD-001", "name": "Premium Cotton T-Shirt", "price": 1200, "rating": 4.5, "reviews": 234, "image": "👕", "badge": "Flash Sale", "description": "High-quality cotton t-shirt"},
        {"id": "PROD-002", "name": "Wireless Bluetooth Earbuds", "price": 3500, "rating": 4.8, "reviews": 1205, "image": "🎧", "badge": "Free Shipping", "description": "Crystal clear sound quality"},
        {"id": "PROD-003", "name": "Phone Screen Protector", "price": 450, "rating": 4.3, "reviews": 856, "image": "📱", "badge": "Deal", "description": "Tempered glass protector"},
        {"id": "PROD-004", "name": "Portable Power Bank 20000mAh", "price": 2800, "rating": 4.6, "reviews": 3421, "image": "🔋", "badge": "Popular", "description": "Fast charging"},
        {"id": "PROD-005", "name": "USB-C Charging Cable", "price": 350, "rating": 4.4, "reviews": 2156, "image": "🔌", "badge": "Best Seller", "description": "Durable & Fast"},
        {"id": "PROD-006", "name": "Wireless Mouse", "price": 1500, "rating": 4.7, "reviews": 1089, "image": "🖱️", "badge": "Flash Sale", "description": "Ergonomic design"},
        {"id": "PROD-007", "name": "LED Desk Lamp", "price": 2200, "rating": 4.5, "reviews": 467, "image": "💡", "badge": "Free Shipping", "description": "Adjustable brightness"},
        {"id": "PROD-008", "name": "Phone Stand Holder", "price": 600, "rating": 4.4, "reviews": 789, "image": "📐", "badge": "Deal", "description": "Universal compatibility"},
    ]

# --- HEADER ---
st.markdown("""
    <div class="header-nav">
        <div>
            <h1>🛍️ RIYU STORE</h1>
        </div>
        <div style="text-align: right; font-size: 14px;">
            <div>Free Shipping on Orders Above PKR 1000</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SEARCH BAR ---
col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    search_query = st.text_input("🔍 Search products...", placeholder="Search for clothing, electronics, home & more")
with col2:
    st.write("")  # spacing
with col3:
    st.write("")  # spacing

# --- PROMO BANNER ---
st.markdown("""
    <div class="promo-banner">
        ⚡ FLASH SALE! Save up to 50% on selected items! Limited time offer
    </div>
""", unsafe_allow_html=True)

# --- TAB NAVIGATION ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "🛒 Cart", "📋 Checkout", "💬 Support", "👤 Account"])

# --- TAB 1: HOME / SHOP ---
with tab1:
    st.subheader("Featured Products")
    
    # Filter products based on search
    filtered_products = st.session_state.products
    if search_query:
        filtered_products = [p for p in st.session_state.products 
                           if search_query.lower() in p['name'].lower()]
    
    # Display products in grid
    cols = st.columns(4)
    for idx, product in enumerate(filtered_products):
        with cols[idx % 4]:
            st.markdown(f"""
                <div class="product-card">
                    <div class="product-image">{product['image']}</div>
                    <div class="product-info">
                        <div style="margin-bottom: 5px;">
                            <span class="badge-{product['badge'].lower().replace(' ', '-')}">{product['badge']}</span>
                        </div>
                        <div class="product-name">{product['name']}</div>
                        <div class="product-price">PKR {product['price']:,}</div>
                        <div class="product-rating">
                            ⭐ {product['rating']} ({product['reviews']} reviews)
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Add to Cart", key=f"add_{product['id']}", use_container_width=True):
                    # Add to cart
                    st.session_state.cart.append({
                        "id": product['id'],
                        "name": product['name'],
                        "price": product['price'],
                        "quantity": 1,
                        "image": product['image']
                    })
                    st.success(f"✅ {product['name']} added to cart!")
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                if st.button("❤️", key=f"fav_{product['id']}", use_container_width=True):
                    st.info("Added to favorites!")

# --- TAB 2: SHOPPING CART ---
with tab2:
    st.subheader("🛒 Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Start shopping! 🛍️")
        st.markdown("""
            <div style="text-align: center; padding: 40px;">
                <h2>Your cart is waiting!</h2>
                <p>Continue shopping to add items to your cart.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Items in Cart:**")
            total_price = 0
            for idx, item in enumerate(st.session_state.cart):
                col_item1, col_item2, col_item3, col_item4 = st.columns([1, 3, 1, 1])
                
                with col_item1:
                    st.write(item['image'])
                
                with col_item2:
                    st.write(f"**{item['name']}**")
                    st.write(f"PKR {item['price']:,}")
                
                with col_item3:
                    quantity = st.number_input("Qty", value=item['quantity'], min_value=1, key=f"qty_{idx}")
                    st.session_state.cart[idx]['quantity'] = quantity
                
                with col_item4:
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                
                total_price += item['price'] * item['quantity']
                st.divider()
        
        with col2:
            st.markdown(f"""
                <div class="cart-sidebar">
                    <div class="cart-header">Order Summary</div>
                    <div style="margin: 15px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>Subtotal:</span>
                            <span><strong>PKR {total_price:,}</strong></span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>Shipping:</span>
                            <span><strong style="color: #10B981;">FREE</strong></span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>Tax:</span>
                            <span><strong>PKR 0</strong></span>
                        </div>
                    </div>
                    <div class="cart-total">
                        <div style="display: flex; justify-content: space-between;">
                            <span>Total:</span>
                            <span>PKR {total_price:,}</span>
                        </div>
                    </div>
                    <button class="checkout-btn">Proceed to Checkout</button>
                </div>
            """, unsafe_allow_html=True)

# --- TAB 3: CHECKOUT ---
with tab3:
    if not st.session_state.cart:
        st.warning("Please add items to your cart first!")
    else:
        st.subheader("📋 Checkout")
        
        # Calculate totals
        total_price = sum(item['price'] * item['quantity'] for item in st.session_state.cart)
        shipping_fee = 0 if total_price >= 1000 else 200
        final_total = total_price + shipping_fee
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="checkout-form">', unsafe_allow_html=True)
            
            # Shipping Information
            st.markdown("### 📦 Shipping Information")
            col1a, col1b = st.columns(2)
            with col1a:
                first_name = st.text_input("First Name*", placeholder="e.g., Ahmed")
            with col1b:
                last_name = st.text_input("Last Name*", placeholder="e.g., Khan")
            
            phone = st.text_input("Phone Number*", placeholder="03001234567")
            address = st.text_area("Delivery Address*", placeholder="House #123, Street Name, Area")
            
            col2a, col2b = st.columns(2)
            with col2a:
                city = st.selectbox("City*", ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Other"])
            with col2b:
                postal_code = st.text_input("Postal Code (Optional)")
            
            st.divider()
            
            # Payment Method
            st.markdown("### 💳 Payment Method")
            payment_method = st.radio("Select Payment Method", ["Cash on Delivery (COD)", "JazzCash", "EasyPaisa", "Bank Transfer"], horizontal=False)
            
            if payment_method == "JazzCash":
                jazzcash_acc = st.text_input("JazzCash Account Number")
            elif payment_method == "EasyPaisa":
                easypaisa_acc = st.text_input("EasyPaisa Account Number")
            elif payment_method == "Bank Transfer":
                bank_name = st.text_input("Bank Name")
                account_num = st.text_input("Account Number")
            
            st.divider()
            
            # Promo Code
            st.markdown("### 🎟️ Promo Code (Optional)")
            promo_code = st.text_input("Enter promo code", placeholder="SAVE10")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="cart-sidebar">
                    <div class="cart-header">Order Summary</div>
                    <div style="margin: 15px 0;">
                        <div style="font-size: 13px; margin-bottom: 10px;">
                            <strong>Items ({len(st.session_state.cart)}):</strong>
                        </div>
            """, unsafe_allow_html=True)
            
            for item in st.session_state.cart:
                item_total = item['price'] * item['quantity']
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 5px;">
                        <span>{item['image']} {item['name']} x{item['quantity']}</span>
                        <span>PKR {item_total:,}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; margin: 15px 0; padding: 15px 0; border-top: 1px solid #F5F5F5; border-bottom: 1px solid #F5F5F5; font-size: 13px;">
                            <span>Subtotal:</span>
                            <span>PKR {total_price:,}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px;">
                            <span>Shipping:</span>
                            <span style="color: #10B981; font-weight: bold;">{"FREE" if shipping_fee == 0 else f"PKR {shipping_fee}"}</span>
                        </div>
                    </div>
                    <div class="cart-total">
                        <div style="display: flex; justify-content: space-between;">
                            <span>Total to Pay:</span>
                            <span>PKR {final_total:,}</span>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            
            if st.button("✅ Place Order", use_container_width=True, type="primary"):
                if not all([first_name, last_name, phone, address, city]):
                    st.error("❌ Please fill all required fields (marked with *)")
                else:
                    # Prepare order
                    order_data = {
                        "customer_name": f"{first_name} {last_name}",
                        "customer_phone": phone,
                        "delivery_address": address,
                        "city": city,
                        "product_id": st.session_state.cart[0]['id'],
                        "wholesale_price": total_price * 0.4,  # Example: 40% wholesale
                        "custom_profit": 450.0,
                        "payout_method": payment_method.split()[0],
                        "payout_account": "03235420909"
                    }
                    
                    try:
                        with st.spinner("Processing your order..."):
                            response = requests.post(
                                f"{st.session_state.api_url}/api/place-order",
                                json=order_data,
                                timeout=10
                            )
                        
                        if response.status_code == 200:
                            order_result = response.json()
                            
                            st.markdown(f"""
                                <div class="success-message">
                                    <h3>✅ Order Placed Successfully!</h3>
                                    <p><strong>Order ID:</strong> {order_result['order_id']}</p>
                                    <p><strong>Total Amount:</strong> PKR {final_total:,}</p>
                                    <p><strong>Estimated Delivery:</strong> {order_result['estimated_delivery']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.success("We'll contact you soon to confirm your order!")
                            
                            # Clear cart
                            st.session_state.cart = []
                            time.sleep(2)
                            st.balloons()
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error placing order: {str(e)}")

# --- TAB 4: SUPPORT / CHAT ---
with tab4:
    st.subheader("💬 Customer Support")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Chat with **Asma** - Our AI Customer Care Assistant")
        
        # Chat history display
        chat_container = st.container()
        
        with chat_container:
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            if st.session_state.chat_history:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"""
                            <div style="background: #EE4D2D; color: white; padding: 10px; border-radius: 8px; margin: 10px 0; text-align: right;">
                                <strong>You:</strong> {msg['content']}
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="background: #F5F5F5; color: #232F3E; padding: 10px; border-radius: 8px; margin: 10px 0;">
                                <strong>🤖 Asma:</strong> {msg['content']}
                            </div>
                        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Input
        col_msg, col_btn = st.columns([4, 1])
        with col_msg:
            user_message = st.text_input("Type your message...", placeholder="Ask about products, shipping, returns...")
        with col_btn:
            send = st.button("Send", use_container_width=True)
        
        if send and user_message:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Get AI response
            try:
                payload = {"message": user_message}
                response = requests.post(
                    f"{st.session_state.api_url}/api/ai-customer-care",
                    json=payload,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": data['reply']
                    })
                    st.rerun()
                else:
                    st.error("Error getting response")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.08);">
                <h3 style="color: #232F3E;">📞 Quick Links</h3>
                <div style="margin-top: 15px;">
                    <div style="margin-bottom: 10px; padding: 10px; background: #F5F5F5; border-radius: 4px;">
                        <strong>📧 Email:</strong><br/>support@riyustore.pk
                    </div>
                    <div style="margin-bottom: 10px; padding: 10px; background: #F5F5F5; border-radius: 4px;">
                        <strong>📱 WhatsApp:</strong><br/>+92 300 1234567
                    </div>
                    <div style="margin-bottom: 10px; padding: 10px; background: #F5F5F5; border-radius: 4px;">
                        <strong>🕐 Hours:</strong><br/>9 AM - 9 PM (Daily)
                    </div>
                </div>
                <h3 style="color: #232F3E; margin-top: 20px;">❓ FAQs</h3>
                <ul style="font-size: 12px; line-height: 1.8;">
                    <li>How long is delivery?</li>
                    <li>What's your return policy?</li>
                    <li>Do you offer COD?</li>
                    <li>How to track order?</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# --- TAB 5: ACCOUNT ---
with tab5:
    st.subheader("👤 My Account")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📦 My Orders")
        if st.session_state.cart:
            st.info("You have recent orders. They will appear here once placed.")
        else:
            st.info("No orders yet. Start shopping!")
        
        st.markdown("### ❤️ My Wishlist")
        st.info("Add items to your wishlist by clicking the heart icon!")
        
        st.markdown("### 💳 Payment Methods")
        if st.button("Add Payment Method", use_container_width=True):
            st.info("Payment methods management coming soon!")
    
    with col2:
        st.markdown("### 👤 Profile Information")
        if st.button("Edit Profile", use_container_width=True):
            st.info("Profile editing coming soon!")
        
        if st.button("Addresses", use_container_width=True):
            st.info("Manage your saved addresses coming soon!")
        
        if st.button("Account Settings", use_container_width=True):
            st.info("Settings management coming soon!")
        
        st.divider()
        if st.button("📞 Customer Support", use_container_width=True):
            st.switch_page("pages/support.py") if "pages" in dir(st) else st.info("Visit Support tab!")
        
        if st.button("Logout", use_container_width=True):
            st.info("Logout coming soon!")

# --- FOOTER ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; padding: 30px; font-size: 12px;">
        <p style="margin: 5px 0;">🛍️ <strong>RIYU STORE</strong> - Pakistani E-Commerce Platform</p>
        <p style="margin: 5px 0;">Free Shipping | Easy Returns | 24/7 Support</p>
        <p style="margin: 5px 0;">© 2026 All Rights Reserved | <a href="https://github.com/rayyan2012lifetime-creator/riyu-store">GitHub</a></p>
        <p style="margin: 15px 0; color: #999;">Powered by FastAPI & Streamlit | AI Customer Support by OpenAI</p>
    </div>
""", unsafe_allow_html=True)
