# CatchData 專案

這個專案可以幫助你自動從指定的 URL 中抓取數據並生成報告。報告將會保存到 `Data` 資料夾中。

## 先決條件

在開始之前，請確保你已經安裝了以下軟體：

- Python 3.6 或以上版本
- `pip3`

## 安裝步驟

1. clone 這個 Repo 到本地端：
   ```sh
   git clone <你的倉庫網址>
   ```
2. 進入到 `CatchData` 資料夾：

   ```sh
   cd CatchData
   ```

3. 安裝所需的 Python 套件：
   ```sh
   pip install -r requirements.txt
   ```

## 執行專案

1. 確保你在 `CatchData` 資料夾中。
2. 使用以下命令來執行程式：

   ```sh
   python3 main.py
   ```

3. 當程式執行時，會要求你輸入一個 URL。輸入你想要抓取數據的 URL 並按下 Enter 鍵。
4. 程式將會開始抓取數據並生成報告。完成後，報告會自動保存到 `Data` 資料夾中。

- 如果有跳出錯誤提示，那就缺什麼裝什麼，都用 pip3 或 pip install 去裝即可
