import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Đọc dữ liệu từ các tệp Excel
df_info_singapore = pd.read_excel('./SINGAPORE2023-data.xlsx', sheet_name='Info')
df_price_singapore = pd.read_excel('SINGAPORE2023-data.xlsx', sheet_name='Price')
df_info_taiwan = pd.read_excel('TW2023-data.xlsx', sheet_name='Info')
df_price_taiwan = pd.read_excel('TW2023-data.xlsx', sheet_name='Price')
df_info_vietnam = pd.read_excel('VN2023-data.xlsx', sheet_name='Info')
df_ticker_vietnam = pd.read_excel('VN2023-data.xlsx', sheet_name='Ticker')

# Kết hợp thông tin từ các sheet
df_singapore = pd.merge(df_info_singapore, df_price_singapore, on='Name')
df_taiwan = pd.merge(df_info_taiwan, df_price_taiwan, on='Name')
df_vietnam = pd.merge(df_info_vietnam, df_ticker_vietnam, on='Name')

# Tạo ứng dụng Dash
app = dash.Dash(__name__)

# Tạo giao diện người dùng
app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': 'Singapore', 'value': 'Singapore'},
            {'label': 'Taiwan', 'value': 'Taiwan'},
            {'label': 'Vietnam', 'value': 'Vietnam'}
        ],
        value='Singapore'
    ),
    dcc.Input(id='symbol-input', type='text', placeholder='Nhập Symbol'),
    html.Div(id='output-data')
])

# Xử lý sự kiện khi người dùng chọn quốc gia và nhập Symbol
@app.callback(
    Output('output-data', 'children'),
    Input('country-dropdown', 'value'),
    Input('symbol-input', 'value')
)
def update_output(selected_country, symbol):
    if selected_country == 'Singapore':
        df = df_singapore
        filename = 'SINGAPORE2023-data.xlsx'
    elif selected_country == 'Taiwan':
        df = df_taiwan
        filename = 'TW2023-data.xlsx'
    elif selected_country == 'Vietnam':
        df = df_vietnam
        filename = 'VN2023-data.xlsx'
    else:
        return "Chọn một quốc gia để truy cập dữ liệu."

    if symbol is not None:
        if symbol in df['Symbol'].values:
            data = df[df['Symbol'] == symbol]
            data = data.select_dtypes(include='float64')
            data = data.melt()  # Chuyển dữ liệu thành dạng dọc

            # Sử dụng HTML để đặt tên cho cột và thiết lập CSS
            data_text = data.to_string(index=False, header=False)
            data_text = "Ngày Giá đóng cửa\n" + data_text  # Bỏ <strong>

            return html.Pre(data_text, style={'white-space': 'pre-wrap'})
        else:
            return "Không tìm thấy Symbol trong dữ liệu."

    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
