import streamlit as st
import requests

def search_products(query):
    encoded_query = requests.utils.quote(query)
    url = f'https://api.digikala.com/v1/search/?q={encoded_query}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise error if request fails
    data = response.json()
    products = data['data']['products']
    results = []
    for p in products:
        title = p['title_fa']
        price = p['default_variant']['price']['selling_price'] // 10  # Integer division for Toman
        link = 'https://www.digikala.com' + p['url']['uri']
        seller = p['default_variant']['seller'].get('title', 'نامشخص')
        specs = {
            'گارانتی': p['default_variant'].get('warranty', {}).get('title_fa', 'نامشخص'),
            'رنگ‌ها': ', '.join([c['title'] for c in p.get('colors', [])]) or 'نامشخص',
            # می‌توانید مشخصات بیشتری اضافه کنید اگر لازم باشد
        }
        results.append({
            'title': title,
            'price': price,
            'specs': specs,
            'link': link,
            'seller': seller
        })
    return results

st.set_page_config(page_title="جستجوی محصولات", page_icon="🔍", layout="wide")

st.title('🔍 جستجوی محصولات در سایت‌های مرجع ایرانی')
st.markdown("این برنامه محصولات را از دیجی‌کالا جستجو می‌کند و قیمت، مشخصات و لینک فروشگاه را نمایش می‌دهد.")

query = st.text_input('نام محصول را وارد کنید (مثال: موبایل سامسونگ):', '')

if st.button('جستجو', type="primary"):
    if query:
        with st.spinner('در حال جستجو... ⌛'):
            try:
                products = search_products(query)
                if not products:
                    st.info("هیچ محصولی یافت نشد.")
                else:
                    for p in products:
                        with st.expander(p['title'], expanded=False):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**قیمت:** {p['price']:,} تومان")
                                st.write(f"**فروشگاه:** {p['seller']}")
                                st.write("**مشخصات:**")
                                for k, v in p['specs'].items():
                                    st.write(f"- {k}: {v}")
                                st.markdown(f"[مشاهده محصول در دیجی‌کالا]({p['link']})")
                            with col2:
                                # اگر بخواهید تصویر اضافه کنید (اختیاری)
                                pass
                        st.divider()
            except Exception as e:
                st.error(f'خطا در جستجو: {str(e)}. لطفاً دوباره امتحان کنید.')
    else:
        st.warning('لطفاً نام محصول را وارد کنید.')

# اضافه کردن زیبایی‌های بیشتر
st.sidebar.title("درباره برنامه")
st.sidebar.info("این برنامه با Streamlit ساخته شده و از API غیررسمی دیجی‌کالا استفاده می‌کند. برای سایت‌های دیگر می‌توانید گسترش دهید.")
st.sidebar.markdown("**نکته:** این برنامه فقط برای اهداف آموزشی است و ممکن است API تغییر کند.")