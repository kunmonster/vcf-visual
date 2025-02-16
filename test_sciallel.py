
import allel
import time

from matplotlib import axis
import numpy


# 应该根据入参来决定需要将哪些字段加入到data中
start_time = time.time()
callset = allel.read_vcf('/home/fkj/py_project/statvcf-sv/example/data/delly_with_duphold.vcf',fields="*")

print(callset.keys())
end_time = time.time()
# print(callset["variants/END"])
print("耗时: {:.2f}秒".format(end_time - start_time))


print(callset["variants/CHROM"])

# genotypes = allel.GenotypeArray(callset['calldata/GT'])

# missing_per_variant = allel.GenotypeArray(callset['calldata/GT']).is_missing().sum(axis=1)
# # 计算总样本数
# n_samples = genotypes.n_samples
# # 计算缺失率（每个位点）
# missing_rate_per_variant = missing_per_variant / n_samples
# print(missing_rate_per_variant)



