# Mitogenome_assembler
This assembler is developped to de novo assemble plant mitochondrial genomes

Our mitogenome assembly pipeline uses whole-genome HiFi sequencing data as input and outputs a complete mitogenome sequence. 

Figure 1 shows the workflow of our assembly pipeline which has five main following steps:

#Step 1. Read correction
	Correct the input data using Canu correct module or other long-reads correct tools if the input data was not generated from PacBio HiFi sequencing technology. 

#Step 2. Data preprocessing
	Since the assembly tool Newbler v.3.0 can only accept high-fidelity reads of less than 30 kb, the Perl script (PacBio_to_Newbler.pl) was used to interrupt the long HiFi or corrected reads (>30 kb) into more reads with different step lengths (default:20 kb).

#Step 3. De novo assembly using Newbler v.3.0
	The preprocessed data was de novo assembled using Newbler v.3.0 with the following parameters: 
	runAssembly -cpu 10 -het -sio -m -urt -large -s 100 -nobig -o $output_dir $input_file
	The input_file is the preprocessed HiFi data in FASTA format, and the output_dir is the name of the result directory. 

#Step 4. Selecting extended seed contigs
	As shown in Figure 2, the longest 3~5 contigs with appropriate depth are selected as extended seeds.

#Step 5. Extending seed contigs and constructing initial assembly graph
	The Python3 script named Get_mitogenome_from_assembly.py was used to extend the seed contigs to capture all target mitochondrial contigs. The resulting GFA format file can be used to construct the initial assembly graph using Bandage.

#Step 6. Visualizing and simplifying assembly graph
	Removing full-path cp contigs and tip contigs (Figure 3).

#Step 7. Exporting the final complete mitogenome sequence using Bandage

