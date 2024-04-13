import quant
from pathlib import Path
from quant.football.data.utils import train_test
from quant.football.transforms import table20240410 as table_factory
from quant.utils.io import load_pkl, make_dir, save_json, save_pkl
print(f"{quant.__version__=}")


def make_datasets(file, date_min, date_sep, date_max, name_suffix, stages, encoder, whole, nc, transforms):
    # 加载数据
    dataset = load_pkl(file)
    print(f"[1] {len(dataset)=}, {len(dataset[0])=}")

    # 检测得分数据是否对齐
    good_data, bad_data, bad_info = table_factory.check_samples(dataset)
    print(f"[2] {len(good_data)=}, {len(bad_data)=}, {bad_info[:3]}")

    # 拆分训练与测试数据子集
    train_data, test_data = train_test(good_data, date_sep, date_min, date_max)
    print(f"[3] {len(train_data)=}, {len(test_data)=}")

    # 忽略比赛不足`n`场的球队比赛
    train_data = table_factory.filter_samples(train_data, limit=6)
    print(f"[4] {len(train_data)=}")

    # 准备数据目录
    out_dir = Path(file).parent.as_posix() + name_suffix
    out_dir = make_dir(out_dir, exist_ok=False)

    # 转换并导出训练数据集(按需计算预处理参数)
    X, Y, Z, stages, encoder, whole, nc, transforms = table_factory.export_dataset(train_data, stages, encoder, whole, nc, transforms)
    print(f"[Train] save {len(X)} rows, {len(X[0])} cols, season {encoder['season']['__len__']}, team {encoder['team']['__len__']}")
    save_pkl(out_dir / "train.pkl", [X, Y, Z])

    # 转换并导出测试数据集(使用训练数据集的预处理参数)
    X, Y, Z, stages, encoder, whole, nc, transforms = table_factory.export_dataset(test_data, stages, encoder, whole, nc, transforms)
    print(f"[Test] save {len(X)} rows, {len(X[0])} cols, season {encoder['season']['__len__']}, team {encoder['team']['__len__']}")
    save_pkl(out_dir / "test.pkl", [X, Y, Z])

    # 保存预处理参数
    save_json(out_dir / "preprocess.cfg", [stages, encoder, whole, nc, transforms])

    return out_dir


# 转换特征+拆分数据集+导出数据到文件
file = "runs/table20240410_2201to2312/samples.pkl"

date_min = "2022-01-01"
date_sep = "2023-11-01"
date_max = "2024-01-01"

name_suffix = "_train_2201_2310_2312_s5_label_whole_c15_maxabs"
stages, encoder, whole, nc, transforms = 5, "label", True, 15, "maxabs"

make_datasets(file, date_min, date_sep, date_max, name_suffix, stages, encoder, whole, nc, transforms)
