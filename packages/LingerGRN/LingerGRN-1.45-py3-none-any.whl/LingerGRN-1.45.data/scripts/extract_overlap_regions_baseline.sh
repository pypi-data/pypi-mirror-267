GRNdir=$1
genome=$2
outdir=$3
mkdir $outdir
cat data/Peaks.txt |sed '1d' |sed 's/:/\t/g'| sed 's/-/\t/g' > $outdir/Region.bed
for i in $(seq 1 22); do
bedtools intersect -a "$GRNdir/${genome}_Peaks_chr$i.bed" -b $outdir/Region.bed -wa -wb > $outdir/"Region_overlap_chr$i.bed"
done
i=X
bedtools intersect -a "$GRNdir/${genome}_Peaks_chr$i.bed" -b $outdir/Region.bed -wa -wb > $outdir/"Region_overlap_chr$i.bed"

