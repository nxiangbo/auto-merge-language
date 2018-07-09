# auto-merge-language

auto-merge-language是自动替换Android项目中的`strings.xml`多语文案工具。

## 使用

打开`config.py`文件，修改路径的前缀和路径后缀。如下所示

```java
    # 项目的工程文件目录前缀
    target_prefix = "/**/**/**"
    # 多语文案所在目录前缀
    src_prefix = "/**/**/**"
    
    # 项目的工程文件目录后缀
    target_suffix = "/strings.xml"
    # 多语文案所在目录后缀
    src_suffix = "/text.xml"
    
``` 

运行`python auto-merge-language`。

## License

Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

