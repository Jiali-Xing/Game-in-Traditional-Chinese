# Game-in-Traditional-Chinese
程式碼，來儘可能的為「沒有繁體中文的遊戲」提供繁體中文支持。

---
# Desperados - 繁體中文補丁
第一個 Use Case 是將 *Desperados* 轉換為繁體中文的程式碼。
它的文本是明文存儲的，並且是用 txt 格式存儲的。這些文件中包含了簡體中文的文本。我們可以使用 `opencc` 來將這些簡體中文轉換為繁體中文。
```opencc -i text_Chinese.txt.bak  -o text_Chinese.txt  -c /usr/share/opencc/s2hk.json```
這個命令會將簡體中文的文本轉換為繁體中文的文本，並且會覆蓋原來的文件。

---
# Until Then - 繁體中文補丁
The second Use Case is to convert *Until Then* into Traditional Chinese.
第二個 Use Case 是將 *Until Then* 轉換為繁體中文的程式碼。

## 理解遊戲文件
首先，這個遊戲的文件結構是這樣的：
```
UntilThen.pck and other files
```
它的遊戲文件是用 PCK 格式打包的，這是一種常見的遊戲資源包格式。我們需要將這個 PCK 文件解包，然後將其中的 JSON 文件轉換為繁體中文，最後再將它們打包回去。
解包後的文件結構如下：
```
UntilThen.pck
├── assets
│   ├── databases
│   │   ├── *json
```
通過`find ./extracted/ -type f -name '*json' -exec grep "我" {} +;` 我們可以找出包含中文的文件。這些文件中有一些是簡體中文的，有一些是日文的。
其他格式的文件（如 inkb）則是用來存儲遊戲的對話和劇情的。這些文件的內容是二進制的，無法直接轉換為繁體中文……這些對話沒有辦法了，只能用簡體中文或者英文了。

## 轉換簡體中文為繁體中文
這個遊戲的長文檔是用 JSON 格式存儲的，這些文件中包含了簡體中文的文本。我們可以使用 `opencc` 來將這些簡體中文轉換為繁體中文。
具體來說，可以通過以下命令來實現：

## Setup
首先，請確保你已經安裝了以下的依賴： python opencc 和 godotpcktool。
```bash
# Install dependencies
sudo pacman -Syu python-pip
pip install --user opencc-python-reimplemented
```
1. Download the game from [Steam], for example, UntilThen is a game that provides only Simplified Chinese.
2. Download the [godotpcktool] from [GitHub] and place it in `~/Applications/`.

## Usage
```bash
# 1. Extract the original PCK
./godotpcktool ~/.local/share/Steam/steamapps/common/Until\ Then/UntilThen.pck -a e -o extracted

# 2. Batch-convert all *_zh-CN.json to HK Traditional (in-place)
python convert_db_zhcn_to_hk_handling_bom.py \
  --db-dir extracted/assets/databases \
  --pattern '*_zh-CN.json'

# 3. Rename files to remove the _zh-CN suffix
# 因為很多文檔不是json格式，所以其實只有部分文件被轉化成了繁體中文，大部分對話文件還是簡體中文的。（inkb格式的文件）
# 如果想要將對話保留為英文，那麼可以用繁體中文的json文件來替換英文的json文件。並且將遊戲設置成英文。
# 如果不介意繁簡混用，請跳過下面這三行並使用簡體中文來運行遊戲。
for f in extracted/assets/databases/*_zh-CN.json; do
  mv -- "$f" "${f%_zh-CN.json}.json"
done

# 4. 將轉換後的json文件添加到PCK中
# from the PCK’s folder:
files=$(find extracted/assets/databases -name '*.json' | paste -sd, -)

~/Applications/godotpcktool \
  --pack "UntilThen.pck" \
  --action add \
  --remove-prefix extracted \
  --file "$files"
```

到此為止，遊戲的長文檔的中文已經轉換為繁體中文了。而其他文字，取決於你的語言設置。