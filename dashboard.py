import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai

st.set_page_config(
    page_title="BMW 상품정보 대시보드",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def check_gemini_api():
    """Gemini API 검증 (Streamlit 재실행 중에도 한 번만 실행)"""
    api_key = None

    # Streamlit Cloud의 secrets 먼저 시도
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        print("[OK] API Key loaded from Streamlit Cloud Secrets")
    except (KeyError, AttributeError):
        # 로컬 환경에서는 .env 파일 사용
        env_path = Path(__file__).parent / '.env'
        load_dotenv(str(env_path), override=True)
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            print("[OK] API Key loaded from .env file")

    if api_key and api_key != "your_gemini_api_key_here":
        try:
            genai.configure(api_key=api_key)
            return True
        except Exception as e:
            print(f"[ERROR] genai.configure failed: {e}")
            return False
    return False

gemini_configured = check_gemini_api()

# Gemini 모델 읽기 (Streamlit Cloud 또는 로컬)
gemini_model = "gemini-flash-latest"
try:
    gemini_model = st.secrets["GEMINI_MODEL"]
except (KeyError, AttributeError):
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

st.title("🚗 BMW 상품정보 대시보드")
st.markdown("---")

def generate_data_context(data):
    context = f"""BMW 대시보드 데이터 요약:

    [판매 현황]
    - 총 판매량: {data['sales_month']['Total_Sales'].sum():,.0f}대
    - 총 수익: ${data['sales_month']['Revenue_USD'].sum():,.0f}
    - 평균 월별 판매량: {data['sales_month']['Total_Sales'].mean():,.0f}대

    [모델 정보]
    - 총 모델 수: {len(data['models'])}개
    - 모델: {', '.join(data['models']['Model_Name'].unique())}
    - 가격대: ${data['models']['Price_USD'].min():,.0f} ~ ${data['models']['Price_USD'].max():,.0f}

    [지역별 현황]
    - 운영 지역: {', '.join(data['sales_region']['Region'].unique())}
    - 지역 수: {len(data['sales_region']['Region'].unique())}개

    [재고 현황]
    - 총 재고: {data['inventory']['Stock_Qty'].sum():,.0f}대
    - 가용 재고: {data['inventory']['Available_Qty'].sum():,.0f}대
    - 예약 재고: {data['inventory']['Reserved_Qty'].sum():,.0f}대

    [고객 정보]
    - 누적 고객 수: {len(data['customers']):,.0f}명
    - 평균 만족도: {data['satisfaction']['Overall_Satisfaction'].mean():.1f}/10
    - 제품 품질 만족도: {data['satisfaction']['Quality_Score'].mean():.1f}/10
    - 서비스 만족도: {data['satisfaction']['Service_Score'].mean():.1f}/10
    - 가격 만족도: {data['satisfaction']['Price_Satisfaction'].mean():.1f}/10

    [딜러 및 옵션]
    - 딜러점 수: {len(data['dealers'])}개
    - 제공 옵션: {len(data['options'])}개
    - 옵션별 평균 인기도: {data['options']['Popularity_Score'].mean():.1f}/10

    [경쟁사 분석]
    - 경쟁사 모델 수: {data['competitors']['Competitor_Model'].nunique()}개
    - 경쟁사별 평균 시장점유율: {data['competitors']['Market_Share'].mean():.1f}%
    - 경쟁사별 평균 가격: ${data['competitors']['Avg_Price_USD'].mean():,.0f}
    """
    return context

def query_gemini(user_message, data_context):
    try:
        model = genai.GenerativeModel(gemini_model)

        system_message = f"""당신은 BMW 자동차 판매 대시보드의 AI 어시스턴트입니다.
다음 대시보드 데이터에 기반하여 사용자의 질문에 답변해주세요.
모든 답변은 한국어로 제공하세요.

{data_context}

사용자의 질문에 정확하고 도움이 되는 답변을 제공하세요."""

        response = model.generate_content(
            f"{system_message}\n\n사용자 질문: {user_message}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500
            )
        )
        return response.text
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

# 데이터 로드
@st.cache_data
def load_data():
    data_dir = "bmw_data"

    models = pd.read_csv(f'{data_dir}/bmw_models.csv')
    sales_region = pd.read_csv(f'{data_dir}/sales_by_region.csv')
    sales_month = pd.read_csv(f'{data_dir}/sales_by_month.csv')
    inventory = pd.read_csv(f'{data_dir}/inventory.csv')
    customers = pd.read_csv(f'{data_dir}/customer_info.csv')
    options = pd.read_csv(f'{data_dir}/options.csv')
    dealers = pd.read_csv(f'{data_dir}/dealers.csv')
    dealer_sales = pd.read_csv(f'{data_dir}/sales_by_dealer.csv')
    daily_sales = pd.read_csv(f'{data_dir}/daily_sales.csv')
    satisfaction = pd.read_csv(f'{data_dir}/customer_satisfaction.csv')
    option_sales = pd.read_csv(f'{data_dir}/option_sales.csv')
    competitors = pd.read_csv(f'{data_dir}/competitor_analysis.csv')

    return {
        'models': models,
        'sales_region': sales_region,
        'sales_month': sales_month,
        'inventory': inventory,
        'customers': customers,
        'options': options,
        'dealers': dealers,
        'dealer_sales': dealer_sales,
        'daily_sales': daily_sales,
        'satisfaction': satisfaction,
        'option_sales': option_sales,
        'competitors': competitors
    }

data = load_data()

# 사이드바 필터
with st.sidebar:
    st.header("🔍 필터 설정")

    selected_models = st.multiselect(
        "모델 선택",
        options=data['models']['Model_Name'].unique(),
        default=data['models']['Model_Name'].unique()[:3]
    )

    selected_regions = st.multiselect(
        "지역 선택",
        options=data['sales_region']['Region'].unique(),
        default=data['sales_region']['Region'].unique()
    )

    view_option = st.radio(
        "대시보드 보기",
        ["📊 개요", "💰 판매분석", "📦 재고관리", "😊 고객만족도", "⭐ 옵션분석", "🏆 경쟁분석"]
    )

    st.markdown("---")
    st.header("🤖 AI 어시스턴트")

    if gemini_configured:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        data_context = generate_data_context(data)

        with st.container(border=True):
            st.subheader("대시보드 데이터 문의", divider=False)

            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            user_input = st.chat_input(
                "대시보드에 대해 질문하세요...",
                key="ai_chat_input"
            )

            if user_input:
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input
                })

                with st.chat_message("user"):
                    st.markdown(user_input)

                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    response = query_gemini(user_input, data_context)
                    response_placeholder.markdown(response)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })

            if st.button("🔄 대화 초기화", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.warning(
            "⚠️ Gemini API 설정이 필요합니다.\n\n"
            "1. .env 파일의 GEMINI_API_KEY를 입력하세요\n"
            "2. [Google AI Studio](https://aistudio.google.com/apikey)에서 무료 API 키를 생성할 수 있습니다"
        )

# ==================== 페이지 1: 개요 ====================
if view_option == "📊 개요":
    st.subheader("📊 판매 현황 개요")

    # KPI 메트릭
    col1, col2, col3, col4, col5 = st.columns(5)

    total_sales = data['sales_month']['Total_Sales'].sum()
    total_revenue = data['sales_month']['Revenue_USD'].sum()
    avg_satisfaction = data['satisfaction']['Overall_Satisfaction'].mean()
    total_customers = len(data['customers'])
    total_dealers = len(data['dealers'])

    with col1:
        st.metric("총 판매량", f"{total_sales:,.0f}대")
    with col2:
        st.metric("총 수익", f"${total_revenue:,.0f}")
    with col3:
        st.metric("고객만족도", f"{avg_satisfaction:.1f}/10")
    with col4:
        st.metric("누적고객", f"{total_customers:,.0f}명")
    with col5:
        st.metric("딜러점 수", f"{total_dealers}개")

    st.markdown("---")

    # 모델별 판매량
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("모델별 누적판매량")
        model_sales = data['sales_month'].groupby('Model')['Total_Sales'].sum().sort_values(ascending=False)
        fig_model = px.bar(
            x=model_sales.values,
            y=model_sales.index,
            orientation='h',
            labels={'x': '판매량 (대)', 'y': '모델'},
            color=model_sales.values,
            color_continuous_scale='Blues'
        )
        fig_model.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_model, use_container_width=True)

    with col2:
        st.subheader("월별 판매 추이")
        monthly = data['sales_month'].groupby('Month')['Total_Sales'].sum().reset_index()
        fig_trend = px.line(
            monthly,
            x='Month',
            y='Total_Sales',
            markers=True,
            labels={'Total_Sales': '판매량 (대)', 'Month': '월'},
            title=None
        )
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # 모델 상세 정보
    st.subheader("BMW 모델 라인업")
    model_display = data['models'][['Model_Name', 'Category', 'Engine_Type', 'Horsepower', 'Price_USD']].copy()
    model_display.columns = ['모델명', '카테고리', '엔진타입', '마력(hp)', '가격($)']
    st.dataframe(model_display, use_container_width=True, hide_index=True)

# ==================== 페이지 2: 판매분석 ====================
elif view_option == "💰 판매분석":
    st.subheader("💰 판매 상세분석")

    col1, col2 = st.columns(2)

    # 지역별 판매
    with col1:
        st.subheader("지역별 총판매량")
        region_data = []
        for region in selected_regions:
            region_sales = data['sales_month'][
                (data['sales_month']['Model'].isin(selected_models))
            ]['Total_Sales'].sum()
            region_data.append({'Region': region, 'Sales': region_sales})

        region_df = pd.DataFrame(region_data).sort_values('Sales', ascending=False)
        fig_region = px.pie(
            region_df,
            values='Sales',
            names='Region',
            title='지역별 판매 비중'
        )
        fig_region.update_layout(height=400)
        st.plotly_chart(fig_region, use_container_width=True)

    # 카테고리별 판매
    with col2:
        st.subheader("카테고리별 판매량")
        cat_sales = data['sales_month'].merge(
            data['models'][['Model_Name', 'Category']],
            left_on='Model',
            right_on='Model_Name'
        )
        cat_data = cat_sales.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
        fig_cat = px.bar(
            x=cat_data.index,
            y=cat_data.values,
            labels={'x': '카테고리', 'y': '판매량 (대)'},
            color=cat_data.values,
            color_continuous_scale='Greens'
        )
        fig_cat.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # 선택된 모델의 월별 판매 추이
    st.subheader(f"선택 모델 월별 판매 추이")
    selected_model_sales = data['sales_month'][
        data['sales_month']['Model'].isin(selected_models)
    ].groupby(['Month', 'Model'])['Total_Sales'].sum().reset_index()

    fig_model_trend = px.line(
        selected_model_sales,
        x='Month',
        y='Total_Sales',
        color='Model',
        markers=True,
        labels={'Total_Sales': '판매량 (대)', 'Month': '월'},
        title=None
    )
    fig_model_trend.update_layout(height=400)
    st.plotly_chart(fig_model_trend, use_container_width=True)

    st.markdown("---")

    # 판매 목표 달성률
    st.subheader("판매 목표 달성률")
    achievement = data['sales_month'][
        data['sales_month']['Model'].isin(selected_models)
    ].groupby('Month')['Achievement_Rate'].mean().reset_index()

    fig_achievement = px.bar(
        achievement,
        x='Month',
        y='Achievement_Rate',
        labels={'Achievement_Rate': '달성률 (%)', 'Month': '월'},
        color='Achievement_Rate',
        color_continuous_scale='RdYlGn'
    )
    fig_achievement.update_layout(height=400)
    st.plotly_chart(fig_achievement, use_container_width=True)

# ==================== 페이지 3: 재고관리 ====================
elif view_option == "📦 재고관리":
    st.subheader("📦 재고 현황")

    col1, col2, col3 = st.columns(3)

    total_stock = data['inventory']['Stock_Qty'].sum()
    total_available = data['inventory']['Available_Qty'].sum()
    total_reserved = data['inventory']['Reserved_Qty'].sum()

    with col1:
        st.metric("총 재고", f"{total_stock:,.0f}대")
    with col2:
        st.metric("가용 재고", f"{total_available:,.0f}대")
    with col3:
        st.metric("예약 재고", f"{total_reserved:,.0f}대")

    st.markdown("---")

    col1, col2 = st.columns(2)

    # 모델별 재고
    with col1:
        st.subheader("모델별 재고 현황")
        model_inventory = data['inventory'].groupby('Model').agg({
            'Stock_Qty': 'sum',
            'Available_Qty': 'sum'
        }).reset_index()

        fig_inv = px.bar(
            model_inventory,
            x='Model',
            y=['Stock_Qty', 'Available_Qty'],
            barmode='group',
            labels={'value': '재고 (대)', 'variable': '재고유형'},
            color_discrete_map={'Stock_Qty': '#1f77b4', 'Available_Qty': '#2ca02c'}
        )
        fig_inv.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_inv, use_container_width=True)

    # 지역별 재고
    with col2:
        st.subheader("지역별 가용 재고")
        region_inv = data['inventory'].groupby('Region')['Available_Qty'].sum().sort_values(ascending=False)
        fig_reg_inv = px.bar(
            x=region_inv.values,
            y=region_inv.index,
            orientation='h',
            labels={'x': '재고 (대)', 'y': '지역'},
            color=region_inv.values,
            color_continuous_scale='Oranges'
        )
        fig_reg_inv.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_reg_inv, use_container_width=True)

    st.markdown("---")

    # 재고 상세 테이블
    st.subheader("재고 상세 현황")
    inventory_display = data['inventory'].copy()
    inventory_display.columns = ['모델', '지역', '총재고', '예약', '가용재고', '업데이트일']
    st.dataframe(inventory_display, use_container_width=True, hide_index=True)

# ==================== 페이지 4: 고객만족도 ====================
elif view_option == "😊 고객만족도":
    st.subheader("😊 고객만족도 분석")

    col1, col2, col3, col4 = st.columns(4)

    avg_quality = data['satisfaction']['Quality_Score'].mean()
    avg_service = data['satisfaction']['Service_Score'].mean()
    avg_price = data['satisfaction']['Price_Satisfaction'].mean()
    avg_overall = data['satisfaction']['Overall_Satisfaction'].mean()

    with col1:
        st.metric("제품 품질 만족도", f"{avg_quality:.1f}/10")
    with col2:
        st.metric("서비스 만족도", f"{avg_service:.1f}/10")
    with col3:
        st.metric("가격 만족도", f"{avg_price:.1f}/10")
    with col4:
        st.metric("전체 만족도", f"{avg_overall:.1f}/10")

    st.markdown("---")

    col1, col2 = st.columns(2)

    # 만족도 분포
    with col1:
        st.subheader("전체 만족도 분포")
        satisfaction_dist = data['satisfaction']['Overall_Satisfaction'].value_counts().sort_index()
        fig_sat_dist = px.bar(
            x=satisfaction_dist.index,
            y=satisfaction_dist.values,
            labels={'x': '만족도 점수', 'y': '응답 수'},
            color=satisfaction_dist.values,
            color_continuous_scale='Viridis'
        )
        fig_sat_dist.update_layout(height=400)
        st.plotly_chart(fig_sat_dist, use_container_width=True)

    # 모델별 만족도
    with col2:
        st.subheader("모델별 평균 만족도")
        model_sat = data['satisfaction'].groupby('Model')['Overall_Satisfaction'].mean().sort_values(ascending=False)
        fig_model_sat = px.bar(
            x=model_sat.values,
            y=model_sat.index,
            orientation='h',
            labels={'x': '평균 만족도', 'y': '모델'},
            color=model_sat.values,
            color_continuous_scale='Reds'
        )
        fig_model_sat.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_model_sat, use_container_width=True)

    st.markdown("---")

    # 만족도 항목별 비교
    st.subheader("만족도 항목별 평균 점수")
    satisfaction_summary = pd.DataFrame({
        '항목': ['제품 품질', '서비스', '가격', '전체 만족도'],
        '점수': [avg_quality, avg_service, avg_price, avg_overall]
    })

    fig_summary = px.bar(
        satisfaction_summary,
        x='항목',
        y='점수',
        labels={'점수': '평균 점수', '항목': '항목'},
        color='점수',
        color_continuous_scale='Blues'
    )
    fig_summary.update_layout(height=400)
    st.plotly_chart(fig_summary, use_container_width=True)

    st.markdown("---")

    # 추천 의사
    st.subheader("고객 추천 의사")
    recommend_data = data['satisfaction']['Would_Recommend'].value_counts().reset_index()
    recommend_data.columns = ['추천의사', 'count']

    fig_recommend = px.pie(
        recommend_data,
        values='count',
        names='추천의사',
        hole=0.4
    )
    fig_recommend.update_layout(height=400)
    st.plotly_chart(fig_recommend, use_container_width=True)

# ==================== 페이지 5: 옵션분석 ====================
elif view_option == "⭐ 옵션분석":
    st.subheader("⭐ 옵션/사양 분석")

    col1, col2 = st.columns(2)

    # 인기도 순위
    with col1:
        st.subheader("옵션 인기도 순위")
        option_rank = data['options'].sort_values('Popularity_Score', ascending=False)
        fig_pop = px.bar(
            option_rank,
            x='Popularity_Score',
            y='Option_Name',
            orientation='h',
            labels={'Popularity_Score': '인기도 점수', 'Option_Name': '옵션명'},
            color='Popularity_Score',
            color_continuous_scale='Purples'
        )
        fig_pop.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_pop, use_container_width=True)

    # 옵션 카테고리별 판매량
    with col2:
        st.subheader("카테고리별 옵션 판매량")
        cat_sales = data['option_sales'].merge(
            data['options'][['Option_ID', 'Category']],
            left_on='Option_ID',
            right_on='Option_ID'
        ).groupby('Category').size().reset_index(name='판매량')

        fig_cat = px.pie(
            cat_sales,
            values='판매량',
            names='Category'
        )
        fig_cat.update_layout(height=400)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # 옵션 상세 정보
    st.subheader("옵션 상세 정보")
    option_display = data['options'].copy()
    option_display.columns = ['옵션ID', '옵션명', '카테고리', '가격($)', '가용여부', '인기도']
    option_display['가용여부'] = option_display['가용여부'].apply(lambda x: '가능' if x else '불가')
    st.dataframe(option_display, use_container_width=True, hide_index=True)

    st.markdown("---")

    # TOP 옵션 판매
    st.subheader("TOP 10 옵션별 판매")
    top_options = data['option_sales'].groupby('Option_Name').size().nlargest(10).reset_index(name='판매량')
    fig_top = px.bar(
        top_options,
        x='판매량',
        y='Option_Name',
        orientation='h',
        labels={'판매량': '판매 건수', 'Option_Name': '옵션명'},
        color='판매량',
        color_continuous_scale='Greens'
    )
    fig_top.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_top, use_container_width=True)

# ==================== 페이지 6: 경쟁분석 ====================
elif view_option == "🏆 경쟁분석":
    st.subheader("🏆 경쟁사 분석")

    # 경쟁사 시장점유율
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("경쟁사 평균 시장점유율")
        comp_share = data['competitors'].groupby('Competitor_Model')['Market_Share'].mean().sort_values(ascending=False)
        fig_share = px.bar(
            x=comp_share.values,
            y=comp_share.index,
            orientation='h',
            labels={'x': '시장점유율 (%)', 'y': '모델'},
            color=comp_share.values,
            color_continuous_scale='Blues'
        )
        fig_share.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_share, use_container_width=True)

    with col2:
        st.subheader("경쟁사 만족도 비교")
        comp_sat = data['competitors'].groupby('Competitor_Model')['Customer_Satisfaction'].mean().sort_values(ascending=False)
        fig_sat = px.bar(
            x=comp_sat.values,
            y=comp_sat.index,
            orientation='h',
            labels={'x': '평균 만족도', 'y': '모델'},
            color=comp_sat.values,
            color_continuous_scale='Greens'
        )
        fig_sat.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_sat, use_container_width=True)

    st.markdown("---")

    # 월별 경쟁사 점유율 추이
    st.subheader("월별 경쟁사 시장점유율 추이")
    fig_trend = px.line(
        data['competitors'],
        x='Month',
        y='Market_Share',
        color='Competitor_Model',
        markers=True,
        labels={'Market_Share': '시장점유율 (%)', 'Month': '월'}
    )
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # 경쟁사 가격 비교
    st.subheader("경쟁사 평균 가격")
    comp_price = data['competitors'].groupby('Competitor_Model')['Avg_Price_USD'].mean().sort_values(ascending=False)
    fig_price = px.bar(
        x=comp_price.index,
        y=comp_price.values,
        labels={'x': '모델', 'y': '평균 가격 ($)'},
        color=comp_price.values,
        color_continuous_scale='Reds'
    )
    fig_price.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_price, use_container_width=True)

st.markdown("---")
st.caption(f"대시보드 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
