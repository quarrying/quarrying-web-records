[comment]: <> (Question URL: https://www.zhihu.com/question/442359762 )
[comment]: <> "Question Title: 场景文本检测中常用 Precision 等作为评价指标, 为何不用 Average Precision?"
[comment]: <> (Author Name: 采石工)

场景文本检测 (Scene Text Detection) 中常用 Precision, Recall 和 F1-Score 作为评价指标, 为什么不用 AP (Average Precision)?

通用目标检测 (还包括人脸检测等特定目标检测) 任务常用 mAP 或 AP 来评价算法, 但在场景文本检测任务中却直接用 Precision, Recall 和 F1-Score. 所以想请教大家: 场景文本检测选择后者是基于什么原因? 另外这个 Precision, Recall 和 F1-Score 是在什么置信度阈值和 IOU 阈值下得到的? 谢谢!

附: 行人检测中也使用了不同于 mAP 或 AP 的评价指标 (log-average Miss Rate), 但其有很明确的定义且和 AP 的定义很类似 ([2012 TPAMI] Pedestrian detection: An evaluation of the state of the art 中: We use the log-average miss rate to summarize detector performance, computed by averaging miss rate at nine FPPI rates evenly spaced in log-space in the range 1e-2 to 1 (for curves that end before reaching a given FPPI rate, the minimum miss rate achieved is used). )


