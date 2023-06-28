# 我是 Azure云运维管理员，写一个创建 Azure Kubernetes Service集群的 shell 脚本
# 资源组名为 hongkong_aks，选用香港区域
# 创建 AKS 集群，3节点，每个节点规格采用 Standard_D2_v2，均分到 3 个可用区
#!/bin/bash