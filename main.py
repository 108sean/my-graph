import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 및 캐싱
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 YYYYMMDD 형태의 실제 Datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d', errors='coerce')
    
    # 주요 수치 데이터 형변환
    df['일관객'] = pd.to_numeric(df['일관객'], errors='coerce')
    df['누적관객'] = pd.to_numeric(df['누적관객'], errors='coerce')
    df['스크린수'] = pd.to_numeric(df['스크린수'], errors='coerce')
    df['상영횟수'] = pd.to_numeric(df['상영횟수'], errors='coerce')
    
    return df

# 앱 타이틀 영역
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 흥행 추이를 탐색합니다.")

# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

st.divider()

# ==========================================
# [구역 1] 영화별 일일 관객수 추이 (선 그래프)
# ==========================================
st.header("📌 구역 1: 영화별 일일 관객수 추이")

# 영화 선택 드롭다운
movie_list = sorted(df['영화명'].dropna().unique())
selected_movie = st.selectbox("분석할 영화를 선택하세요:", movie_list)

if selected_movie:
    # 선택한 영화 데이터 추출 및 정렬
    movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')
    
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"<{selected_movie}> 날짜별 일관객 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
        markers=True
    )
    
    # 마우스 오버(툴팁) 레이아웃 설정
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객수:</b> %{y:,}명<extra></extra>"
    )
    
    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="관객 수 (명)",
        hovermode="x unified"
    )
    
    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)
    
    # 그래프 설명 문구 출력 위치
    st.info(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 상영 기간 동안 개봉 초기 관객 집중도와 주말/평일 관객수 변화 추이를 한눈에 파악할 수 있습니다.")

st.divider()

# ==========================================
# [구역 2] 추가 그래프 구역 (확장용)
# ==========================================
st.header("📌 구역 2: (추가 예정 구역)")
st.caption("앞으로 새로운 시간 관련 그래프 분석 기능이 이 영역에 추가될 예정입니다.")
