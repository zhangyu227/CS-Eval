---
license: mit
configs:
- config_name: test
  data_files:
  - split: zh
    path: "test_zh.json"
  - split: en
    path: "test_en.json"
  - split: zh_subset
    path: "test_zh_subset.json"
- config_name: dev
  data_files:
  - split: zh
    path: "dev_zh.json"
  - split: en
    path: "dev_en.json"
---

SafetyBench is a comprehensive benchmark for evaluating the safety of LLMs, which comprises 11,435 diverse multiple choice questions spanning across 7 distinct categories of safety concerns. Notably, SafetyBench also incorporates both Chinese and English data, facilitating the evaluation in both languages.

Please visit our [GitHub](https://github.com/thu-coai/SafetyBench) and [website](https://llmbench.ai/safety) or check our [paper](https://arxiv.org/abs/2309.07045) for more details.

We release three differents test sets including Chinese testset (`test_zh.json`), English testset (`test_en.json`) and Chinese subset testset (`test_zh_subset.json`). The Chinese subset testset removes samples with highly sensitive keywords to test API-based Chinese LLMs with strict filtering mechanism. 
We also release 5 examples for each of the 7 safety categories in both Chinese (`dev_zh.json`) and English (`dev_en.json`), to enable few-shot evaluation.

Labels on the test sets are not released and users are required to submit their results to automatically obtain test accuracy. [How to submit?](https://github.com/thu-coai/SafetyBench#how-to-submit)

## Load the Data

```python
from datasets import load_dataset

test_dataset = load_dataset("thu-coai/SafetyBench", "test")
dev_dataset = load_dataset("thu-coai/SafetyBench", "dev")

```

More details about loading the data and evaluating LLMs could be found at our [github repository](https://github.com/thu-coai/SafetyBench).

Please cite our paper if you use our dataset.

```
@article{zhang2023safetybench,
      title={SafetyBench: Evaluating the Safety of Large Language Models with Multiple Choice Questions}, 
      author={Zhexin Zhang and Leqi Lei and Lindong Wu and Rui Sun and Yongkang Huang and Chong Long and Xiao Liu and Xuanyu Lei and Jie Tang and Minlie Huang},
      journal={arXiv preprint arXiv:2309.07045},
      year={2023}
}
```