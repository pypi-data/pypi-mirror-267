# lanQ v1.2

English | [简体中文](README_ZH.md)

Language quality evaluation tool.

## Run it

Clone the project into your environment.

```
git clone ssh://git@gitlab.pjlab.org.cn:1122/qa/lanq.git
```

Install the requirement packages.

```
pip install -r requirements.txt
```

Add the test data file `test_data.json` into `data/predictions` directory.  
Then execute `main.py` with parameter `-i`.

```
python main.py -i test_data.json
```

You will get the result file `data_predictions_test_data.json` in `data/results`.

If you want to test files in directory, you just need to change to file name to directory name in `data/predictions`, such as:

```
python main.py -i directory_name
```

## Data format

There are 2 data format supported.  
One is model type, contain `id`, `prompt` and `prediction` keys, as follows:  

```
{"id": "0", "prompt": "how old are you?", "prediction": "I am 8 years old."}
```

Another is data type, have `id` and `content` keys, such as:

```
{"id":"Bl1b6P41SlcCHv8gfhLy","content":"秦始皇嬴政，从此结束了贵族王侯专政的王国时代，进入了君主专制的帝国时代。"}
```

No matter what data format is, each line of data is `json` type and each data file only has one format data.   
Besides, data exits in data file with `jsonline` style, refering to `test_data1.json` or `test_data2.json`.

## Reading result

The file in `data/results` directory has format as follows:

```
{
    "score": 50.0,
    "num_good": 1,
    "num_bad": 1,
    "total": 2,
    "ERROR_RULE_COLON_END": {
        "count": 1,
        "ratio": 0.5,
        "detail": [
            {
                "id": "0",
                "error_reason": "冒号结尾"
            }
        ]
    },
}
```

key name | description
-|-
`score` | `num_good` / `total`, means the quality of data.  
`num_good` | the count of good data.  
`num_bad` | the count of bad data, which has some error.  
`total` | the count of all data.  
`ERROR_RULE_COLON_END` | the error name.  
`count` | the number of error appearance.    
`ratio` | `count` / `total`, means the ratio of error appearance.  
`detail` | the information of error.  
`id` | the data id with error.  
`error_reason` | the reason why judge the data has error. 

## How to Use

First, you should install the package.

```
pip install lanQ
```

After installing the tool in python environment, wo can import it in our project as follows.

```
from lanQ_rule import common_rule
```

At this time, we can use all functions in `common_rule.py`. The parameter `content` is must `string` type, such as:

```
common_bracket_unmatch(content)
```

We will get a result, which is a json type and has a key `error_status`.  
If `error_status` is `True`, which means content has problem, the result will have other 2 keys: `error_type` and `error_reason`, for example:  

```
{
   'error_status': True, 
   'error_type': 'ERROR_RULE_COLON_END', 
   'error_reason': '冒号结尾'
}
```

## Upload 

Update the version number in `setup.py`

```
setup(
    name="lanQ",
    version="x.y",
    ...
)
```

Make a .tar file for using in other project. 
You will get a .tar file in `lanQ/dist/`

```
python .\setup.py sdist
```

Upload the .tar file to Internet.

```
twine upload .\dist\lanQ-x.y.tar.gz
```

## Summary of Quality Functions

The Category in below table is the same name `.py` file in `lanQ/lanQ_rule/` path.  
Function's name are arranged in alphabetical order.

Function Name | Description                                             | Category | Version
-|---------------------------------------------------------|----------|-
common_anti_crawler_zh | check weather the content contains anti crawl text |  common  |  1.2
common_bracket_unmatch | check whether bracket is matches                        | common   | 1.0
common_chaos_en | check whether content has English messy code            | common   | 1.0
common_chaos_symbol | check whether content has a lot of meaningless words    | common   | 1.0
common_chaos_zh | check whether content has Chinese messy code            | common   | 1.0
common_check_photo | check whether content has photo | common | 1.2
common_colon_end | check whether the last char is ':'                      | common   | 1.0
common_content_null | check whether content is null | common   | 1.0
common_doc_repeat | check whether content repeats                           | common   | 1.0
common_ellipsis_ratio   |  check whether ratio of lines end with ellipsis is bigger than 75% | common | 1.2
common_emoj_characters | check whether content contains emoji charactors | common | 1.2
common_enter_more | check whether content has more than 8 continious enter | common   | 1.0
common_enter_ratio_more | check whether enter / content is more than 25% | common   | 1.0
common_html_entity | check whether content has html entity | common | 1.2
common_img_html_tag | check whether content has img tag or html tag | common | 1.2
common_invalid_web | check whether the content is invalid | common | 1.2 
common_invisible_char | check whether content has invisible char | common | 1.2
common_joint_special_symbol | check if there are special symbols composed of multiple symbols spliced together | common | 1.2
common_language_mixed | check whether content is mixed in Chinese and English   | common   | 1.0
common_license_key | check if the content contains license key| common | 1.2
common_no_punc | check whether content has paragraph without punctuations | common   | 1.0
common_space_more | check whether content has more than 500 space | common   | 1.0
common_special_character | check whether special char in content, such as '�'      | common   | 1.0
common_special_mark | check if the content contains special mark | common |1.2
common_unconverted_symbol | check if the content contains special symbols for conversion failure | common | 1.2
common_underscore_length | check whether the content contains underscores whose length is longer than 15 | common | 1.2
common_url_only | check whether content is all urls | common   | 1.0
common_word_stuck | check whether words are stuck | common   | 1.0
model_advertisement | check whether content has model advertisement | model    | 1.0
model_watermark | check whether content has watermark | model    | 1.0
prompt_chinese_produce_english | check whether chinese prompt produce english prediction | prompt   | 1.0
prompt_english_produce_chinese | check whether english prompt produce chinese prediction | prompt   | 1.0

## RoadMap
 - 1.5:
   - 支持多种数据格式的convert
 - 1.4:
   - 增加函数的可配置性

## Release Notes
 - 1.3:
   - 重新组织 config.py 对外开放用户配置接口
   - 添加 error 比例
   - main 与 convert 模块批量处理
 - 1.2:
   - 更新 main 与 config 模块，使用 callable 组织函数
   - common_rule 添加 v1.2 新规则
   - 新增 convert 目录，支持 stringline 转化；
   - readme 补充使用方法与数据类型
 - 1.1:
   - 新增 base.py 抽取基础功能;
   - functions 按字母顺序排列
 - 1.0:   
   - 新增 1.0 functions;  
   - 新增 common_rule 模块;  
   - 新增 model_rule 模块;  
   - 新增 prompt_rule 模块;  
   - 新增 convert 功能;
   - 新增 main.py 支持本质运行。
