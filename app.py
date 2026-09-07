import streamlit as st
import random
import string

# ---------- CORE LOGIC (same as before) ----------
AMBIGUOUS = set('O0Il1')
UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = string.punctuation

def get_character_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    pool = ""
    if use_upper:
        pool += UPPER
    if use_lower:
        pool += LOWER
    if use_digits:
        pool += DIGITS
    if use_symbols:
        pool += SYMBOLS
    if exclude_ambiguous:
        pool = ''.join(ch for ch in pool if ch not in AMBIGUOUS)
    return pool

def generate_passwords(count, length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    pool = get_character_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)
    if not pool:
        return None, 0, "Error: No character types selected or pool empty!"
    
    # Ensure at least one from each selected type
    required_pools = []
    if use_upper:
        required_pools.append(UPPER if not exclude_ambiguous else ''.join(ch for ch in UPPER if ch not in AMBIGUOUS))
    if use_lower:
        required_pools.append(LOWER if not exclude_ambiguous else ''.join(ch for ch in LOWER if ch not in AMBIGUOUS))
    if use_digits:
        required_pools.append(DIGITS if not exclude_ambiguous else ''.join(ch for ch in DIGITS if ch not in AMBIGUOUS))
    if use_symbols:
        required_pools.append(SYMBOLS if not exclude_ambiguous else ''.join(ch for ch in SYMBOLS if ch not in AMBIGUOUS))
    
    passwords = []
    for _ in range(count):
        password_chars = []
        for p in required_pools:
            if p:
                password_chars.append(random.choice(p))
        remaining = length - len(password_chars)
        if remaining < 0:
            password_chars = password_chars[:length]
        else:
            password_chars.extend(random.choice(pool) for _ in range(remaining))
        random.shuffle(password_chars)
        passwords.append(''.join(password_chars))
    
    return passwords, len(pool), None

def calculate_entropy(password, pool_size):
    if pool_size == 0:
        return 0
    return len(password) * (pool_size.bit_length() - 1)

def strength_rating(entropy):
    if entropy < 28:
        return "Weak 🔴"
    elif entropy < 36:
        return "Moderate 🟡"
    elif entropy < 60:
        return "Strong 🟢"
    else:
        return "Very Strong 💪"

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Password Generator", page_icon="🔐", layout="centered")

st.title("🔐 Powerful Password Generator")
st.markdown("Generate strong, random passwords with custom rules.")

with st.container():
    # Layout using columns
    col1, col2 = st.columns(2)
    with col1:
        length = st.slider("📏 Password Length", min_value=4, max_value=64, value=16)
    with col2:
        count = st.number_input("🔢 Number of Passwords", min_value=1, max_value=10, value=1)

    st.divider()
    
    col3, col4 = st.columns(2)
    with col3:
        use_upper = st.checkbox("✅ Uppercase (A-Z)", value=True)
        use_digits = st.checkbox("✅ Digits (0-9)", value=True)
    with col4:
        use_lower = st.checkbox("✅ Lowercase (a-z)", value=True)
        use_symbols = st.checkbox("✅ Symbols (!@#)", value=True)

    exclude_ambiguous = st.checkbox("🚫 Exclude ambiguous characters (O, 0, I, l, 1)", value=False)

    # Validation check
    if not (use_upper or use_lower or use_digits or use_symbols):
        st.warning("⚠️ Please select at least one character type!")

    generate_btn = st.button("🚀 Generate Passwords", type="primary", use_container_width=True)

# Result area
if generate_btn:
    if not (use_upper or use_lower or use_digits or use_symbols):
        st.error("❌ Cannot generate: No character type selected.")
    else:
        passwords, pool_size, error = generate_passwords(
            count, length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous
        )
        
        if error:
            st.error(f"❌ {error}")
        else:
            st.success(f"✅ Successfully generated {len(passwords)} password(s)!")
            st.divider()
            
            for i, pwd in enumerate(passwords, 1):
                entropy = calculate_entropy(pwd, pool_size)
                rating = strength_rating(entropy)
                
                # Display password with copy button (Streamlit's st.code has built-in copy)
                st.code(pwd, language="text")
                
                # Display metrics
                col_meta1, col_meta2 = st.columns(2)
                with col_meta1:
                    st.metric(label="Entropy", value=f"{entropy:.1f} bits")
                with col_meta2:
                    st.metric(label="Strength", value=rating)
                st.divider()