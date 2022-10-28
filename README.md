# Mitogenome_assembler
This assembler is developped to de novo assemble plant mitochondrial genomes

Our mitogenome assembly pipeline uses whole-genome HiFi sequencing data as input and outputs a complete mitogenome sequence. 

Figure 1 shows the workflow of our assembly pipeline which has five main following steps:
	![image text(https://github.com/bichangwei/Mitogenome_assembler/Figures/Pipeline.jpg)

# Step 1. Read correction using Canu correct module if the input data was not generated from PacBio HiFi sequencing
        canu -correct -p Correct -d PacBio genomeSize=500m rawErrorRate=0.3 correctedErrorRate=0.045 batThreads=20 "batOptions=-dg 3 -db 3 -dr 1 -ca 500 -cp 50" useGrid=false -pacbio PacBio.fastq.gz
        # -p <assembly-prefix>
        # -d <assembly-directory>
        # genomeSize=<number>[g|m|k]
        # rawErrorRate:The allowed difference in an overlap between two raw uncorrected reads. The defaults are 0.300 for PacBio reads
        # correctedErrorRate:The allowed difference in an overlap between two corrected reads. Defaults are 0.045 for PacBio reads

# Step 2. Convert long reads into a new file for Newbler assembly (<30k)
        perl PacBio_to_Newbler.pl -i Hifi.fa -o Hifi.cut20k.fa -b 20000
        # -i <corrected or HiFi fasta file>
        # -o <coverted fasta file>
        # -b Braek the reads (>30k) into more short reads (<20k); default: 20000 bp

# Step 3. De novo assembly using Newbler v.3.0
        runAssembly -cpu 10 -het -sio -m -urt -large -s 100 -nobig -o $output_dir Hifi.cut20k.fa
        # -het: Flag to enable Heterozygotic mode, which causes the assembler to choose a path between 2 contigs when there is ambiguity regarding the path that should be taken.
        #       By default, the assembler will not choose a path when ambiguity exists
        # -sio: Flag to invoke serial I/O. Use for projects with > 4 million reads.
        # -m: Keeps sequence data in memory Increases speed
        # -urt: Extend contigs using the ends (tips) of single reads
        # -large: Speeds up assembly but reduces accuracy
        # -nobig: Skip output of large files (.ace, 454AlignmentInfo.tsv) Default: no
        # -o <output-directory>

# Step 4. Selecting extended seed contigs (longest 3~5 contigs with medium depth)
        awk '{if($2 ~ /^contig/)print}' 454ContigGraph.txt > Species.csv
        # draw coverage distribution graph with Scripts/Plot_coverage.R
	As shown in Figure 2:
	![image text(https://github.com/bichangwei/Mitogenome_assembler/Figures/Je_merge1.jpg)
# Step 5. Extending seed contigs and constructing initial assembly graph
	gunzip Example/Organism/Assembly_result/454AllContigs.fna.gz
        python3 Get_mitogenome_from_assembly.py -c 454ContigGraph.txt -a 454AllContigs.fna -o Assembly_graph.gfa -s 406 501 566 831 1029
        # -c <454ContigGraph.txt> Assembly graph file generated from Newbler
        # -a <454AllContigs.fna> All generated contig sequences
        # -s <seeds> Selected from step4
        # -o <Output graph file> Output file for Step6

# Step 6. Visualizing and simplifying assembly graph using Bandage
        # Open Assembly.gfa with Bandage
        # Remove full-path cp contigs and tip contigsAssembly.gfa
        # Decode the revised assembly graph based on the copy number of each contig
        # Merged all possible nodes and exported the complete mitogenome sequence to a FASTA format file
	As shown in Figure 3:
	![image text(https://github.com/bichangwei/Mitogenome_assembler/Figures/Juncus_effusus_2G.jpg)
#Step 7. Exporting the final complete mitogenome sequence using Bandage
