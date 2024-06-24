### JS 代替 Python 做網頁操作 — 切換視窗 1

```
document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button:nth-child(2)").click();
```

### JS 代替 Python 做網頁操作 — 切換頁面

```
document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div:nth-child(4) > div.pagination-container.d-flex.justify-center > div > button.btn-next").click();
```

### JS 代替 Python 做網頁操作 — 切換視窗 2

```
document.querySelector("#app > div > main > div > div > div.row.detail.common_detail.justify-start.justify-md-center > div.detail_l.col-sm-12.col-md-8.col-lg-9.col-xl-9.col-12 > div.v-window.detail_tab_items.v-item-group.theme--light.v-tabs-items > div > div > div.investment > div.d-flex.flex-row.align-center.justify-space-between > div.d-flex.flex-column.flex-md-row.align-end.align-md-center > div > button.btn.v-btn.v-btn--text.theme--light.v-size--default.active").click();
```

### 待辦清單

- ✅ 輸入網址 zh 自動轉換
- ✅ 產出 CSV Data 換到 Data Folder 當中
- ✅ 加入 catchVCInvestment.py 的項目 Name 到 CSV
- ✅ 加入 catchProjectExchange.py 的 Exchange 數據到 CSV
- 沒有 Token 的 VC 會報錯

### 計數 Selector
