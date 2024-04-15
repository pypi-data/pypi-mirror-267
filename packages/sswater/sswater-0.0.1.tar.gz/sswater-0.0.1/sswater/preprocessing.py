import pandas as pd
from sklearn.preprocessing import StandardScaler


def preprocess(data) :
    data.dropna(inplace=True)
    data.set_index('data_time',inplace=True)
    data.index = pd.to_datetime(data.index)
    data.info()

    columns_to_scale = ['ma_q']
    scaler = StandardScaler()
    scaler2 = StandardScaler()
    data_scaled = scaler.fit_transform(data[columns_to_scale])
    target_scaled = scaler2.fit_transform(data['ma_q'].values.reshape(-1, 1))
    
    # 스케일링된 열을 포함한 DataFrame 생성
    data_scaled_df = pd.DataFrame(data_scaled, columns=columns_to_scale)
    data_scaled_df = data_scaled_df.set_index(data.index)
    data_scaled_df.rename(columns={'ma_q':'learningma_q'},inplace=True)
    
    # 'ma_Q' 열을 추가하여 원본 DataFrame과 병합
    data_scaled_df['ma_q'] = data_scaled_df['learningma_q'] # ma_Q/의 경우 scaling 하지 않고 target으로 사용해봄. <=== 해당 부분 문제 가능성이 있어 주석처리
    data_scaled_df.drop('learningma_q',axis=1, inplace=True)

    features = data_scaled_df.values
    
    return features, scaler2

def correction(data):
    """
    1. db가장최근날짜 - 최종학습날짜 날짜계산 후 곱하기 24시간 개수랑 데이터 개수 비교
    2. 개수가 안맞으면 빈시간대를 추가 유량값 0 
    3. 0 개수 세기 > 7일 전 후 같은 시간대 0이 아닌 유량 평균값으로 보정 
    4. 이상치 확인 후 보정 
    """
    directory = "./example/src/trainedModels/js/"
    with open(directory+'latest_train_date.txt', 'r' ) as f:
            lines = f.readlines()  # 파일의 모든 줄을 읽어옵니다.

            # 첫 번째 행의 날짜와 두 번째 행의 버전 값을 분리
            saved_date = lines[0].strip()
            
    df = pd.DataFrame()

    return df
