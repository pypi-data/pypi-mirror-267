import quant
from pathlib import Path
from quant.football.data.utils import filter_samples, train_test
from quant.football.transforms import table20240410 as table_factory
from quant.utils.io import load_pkl, make_dir, save_json, save_pkl
print(f"{quant.__version__=}")

file = "runs/table20240410_2201to2312/samples.pkl"

# 加载数据
dataset = load_pkl(file)
print(f"[1] {len(dataset)=}, {len(dataset[0])=}")

# 检测得分数据是否对齐
good_row, bad_row, bad_msg = table_factory.check_samples(dataset)
print(f"[2] {len(good_row)=}, {len(bad_row)=}, {len(bad_msg)=}")

# 拆分训练与测试数据子集
train_data, test_data = train_test(good_row, date_sep="2023-11-01", date_min="2022-01-01", date_max="2024-01-01")
print(f"[3] {len(train_data)=}, {len(test_data)=}")

# 忽略比赛不足`n`场的球队比赛
train_data = filter_samples(train_data, team_idxs=[11, 12], limit=6)
print(f"[4] {len(train_data)=}")

# 准备数据目录
out_dir = Path(file).parent.as_posix() + "_train_2201_2310_s5_label_whole_c15_maxabs"
out_dir = make_dir(out_dir, exist_ok=False)

# 导出数据集
stages, encoder, whole, nc, transforms = 5, "label", True, 15, "maxabs"
X, Y, Z, stages, encoder, whole, nc, transforms = table_factory.export_dataset(train_data, stages, encoder, whole, nc, transforms)
print(f"[Train] save {len(X)} rows, {len(X[0])} cols, season {encoder['season']['__len__']}, team {encoder['team']['__len__']}")
save_pkl(out_dir / "train.pkl", [X, Y, Z])
save_json(out_dir / "preprocess.cfg", [stages, encoder, whole, nc, transforms])
X, Y, Z, stages, encoder, whole, nc, transforms = table_factory.export_dataset(test_data, stages, encoder, whole, nc, transforms)
print(f"[Test] save {len(X)} rows, {len(X[0])} cols, season {encoder['season']['__len__']}, team {encoder['team']['__len__']}")
save_pkl(out_dir / "test.pkl", [X, Y, Z])

# 打印输出位置
print(f"\nout_dir:\n{out_dir}")
