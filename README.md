# Game-in-Traditional-Chinese
程式碼，來儘可能的為「沒有繁體中文的遊戲」提供繁體中文支持。
This repo contains scripts and patches to convert *Until Then* into Traditional Chinese.

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