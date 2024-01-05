#!/bin/bash

#Resample

flirt -in small-img -ref small-img -out small_2mm -applyisoxfm 2

flirt -in AAN_DR_MNI152_1mm_v1p0_20150630.nii -ref AAN_DR_MNI152_1mm_v1p0_20150630.nii -out AAN_DR_MNI152_2mm_v1p0_20150630.nii -applyisoxfm 2


flirt -in MNI152_T1_2mm_brain.nii.gz -ref MNI152_T1_2mm_brain.nii.gz -out MNI152_T1_3mm_brain.nii.gz -applyisoxfm 3

flirt -in 03-acq-1mm_T1w_acq-1mm_T1w_20230502163801_3.nii -ref 03-acq-1mm_T1w_acq-1mm_T1w_20230502163801_3.nii -out 03-acq-3mm.nii -applyisoxfm 3

flirt -in brain_highres2standard.nii.gz -ref brain_highres2standard.nii.gz -out brain_highres2standard_3mm.nii.gz -applyisoxfm 3

flirt -in bet_brain_bin.nii.gz -ref bet_brain_bin.nii.gz -out bet_brain_bin_2mm.nii.gz -applyisoxfm 2

flirt -in highres.nii.gz -ref highres.nii.gz -out highres_2mm.nii.gz -applyisoxfm 2

flirt -in highres_bin.nii.gz -ref highres_bin.nii.gz -out highres_bin_2mm.nii.gz -applyisoxfm 2


Conversion dicoms to nifti

dcm2niix folder_input

#chemin

Documents/ImpAcq/ImpAcq_
#creation fieldmap


fsl_prepare_fieldmap <scanner> <phase_image> <magnitude_image> <out_image> <deltaTE (in ms)>

fsl_prepare_fieldmap SIEMENS /10-gre_field_mapping/10-gre_field_mapping_gre_field_mapping_20230613161014_10_e2_ph.nii /09-gre_field_mapping/09-gre_field_mapping_gre_field_mapping_20230613161014_9_e1.nii fmap_rads 2.97

betechobrain.nii.gz
10-gre_field_mapping_gre_field_mapping_20230613161014_10_e2_ph.nii

fsl_prepare_fieldmap SIEMENS 10-gre_field_mapping_gre_field_mapping_20230616153524_10_e2_ph.nii betechobrain.nii.gz fmap_rads 2.46


#Sans le filedmap déjà calculé
fugue -i 04-func_task-anagrams_run-1_func_task-anagrams_run-1_20230613161014_4.nii -p fmap_rads.nii.gz --dwell=0.0000026 --asym=0.00246 -s 0.5 -u result

2.6e-06
0.000026
#fieldmap preload
fugue -i 12-func_task-rest_func_task-rest_20230613161014_12.nii --dwell=0.000719992 --loadfmap=fmap_rads.nii.gz -u result




#Automatisation création fieldmap  + correction EPI

cd
cd documents/ImpAcq
for i in `seq -w 14 14`; do
	cd ImpAcq_${i}
	if test ! -e fmap_9_10 ; then
		mkdir fmap_9_10
	fi
	if test ! -e fmap_14_15 ; then
		mkdir fmap_14_15
	fi
	cd fmap_9_10
	cp ../09-gre_field_mapping/09-gre_field_mapping_gre_field_mapping_*.nii .
	cp ../10-gre_field_mapping/10-gre_field_mapping_gre_field_mapping_*.nii .
	bet 09-gre_field_mapping_gre_field_mapping_*1.nii betechobrain -f 0.4
	fsl_prepare_fieldmap SIEMENS 10-gre_field_mapping_gre_field_mapping_*.nii betechobrain.nii.gz fmap_rads 2.46
	cd ..
	cd fmap_14_15
	cp ../14-gre_field_mapping/14-gre_field_mapping_gre_field_mapping_*.nii .
	cp ../13-gre_field_mapping/13-gre_field_mapping_gre_field_mapping_*1.nii .
	bet 13-gre_field_mapping_gre_field_mapping_*1.nii betechobrain -f 0.4
	fsl_prepare_fieldmap SIEMENS 14-gre_field_mapping_gre_field_mapping_*.nii betechobrain.nii.gz fmap_rads 2.46
	cd ../..
done


cd
cd documents/ImpAcq
for i in `seq -w 1 12`; do
	cd ImpAcq_${i}
	cd fmap_9_10
	bet 09-gre_field_mapping_gre_field_mapping_*1.nii betechobrain -f 0.4
	fsl_prepare_fieldmap SIEMENS 10-gre_field_mapping_gre_field_mapping_*ph.nii betechobrain.nii.gz fmap_rads 2.46
	cd ..
	cd fmap_14_15
	bet 13-gre_field_mapping_gre_field_mapping_*1.nii betechobrain -f 0.4
	fsl_prepare_fieldmap SIEMENS 14-gre_field_mapping_gre_field_mapping_*ph.nii betechobrain.nii.gz fmap_rads 2.46
	cd ../..
done




cd
cd documents/ImpAcq
for i in `seq -w 1 8`; do
	cd ImpAcq_0${i}
	cd fmap_9_10
	bet 09-gre_field_mapping_gre_field_mapping_*_e1.nii betechobrain -f 0.4
	fsl_prepare_fieldmap SIEMENS 10-gre_field_mapping_gre_field_mapping_*.nii betechobrain fmap_rads 2.46
	cd ../..
done

#Creation fieldmap en rad/s
cd
cd documents/ImpAcq
for i in `seq -w 4 4`; do
	cd ImpAcq_0${i}
	cd fmap_9_10
	bet 13-gre_field_mapping_gre_field_mapping_*1.nii betechobrain -f 0.4
	fsl_prepare_fieldmap SIEMENS 14-gre_field_mapping_gre_field_mapping_*.nii betechobrain fmap_rads 2.46
	cd ../..
done



fugue -i 04-func_task-anagrams_run-1_func_task-anagrams_run-1_20230616153524_4.nii --dwell=0.000560006 --loadfmap=../fmap_9_10/fmap_rads.nii.gz --unwarpdir='y-' -u corrected_epi

#Correction de EPI avec fieldmap créée  + decompression fichier tar
cd
cd documents/ImpAcq
for i in `seq -w 9 11`; do
	cd ImpAcq_${i}
	for j in `seq -w 1 5`; do
		cd *-func_task-anagrams_run-${j}
		fugue -i *-func_task-anagrams_run-${j}_func_task-anagrams_run-${j}_*$((j+3)).nii --dwell=0.000560006 --loadfmap=../fmap_9_10/fmap_rads.nii.gz --unwarpdir='y-' -u corrected_epi
		gzip -d corrected_epi.nii.gz
		cd ..
	done
	cd ..
done

fsl_prepare_fieldmap SIEMENS 14-gre_field_mapping_gre_field_mapping_*.nii betechobrain fmap_rads 2.46

fugue -i 05-func_task-anagrams_run-2_func_task-anagrams_run-2_20230616153524_5.nii --dwell=0.000250006 --loadfmap=../fmap_9_10/fmap_rads.nii.gz --unwarpdir='y-' -u corrected_epi
#même chose pour le RS
cd
cd documents/ImpAcq
for i in `seq -w 14 14`; do
	cd ImpAcq_${i}
	cd 12-func_task-rest
	fugue -i 12-func_task-rest*14.nii --dwell=0.000719992 --loadfmap=../fmap_14_15/fmap_rads.nii.gz --unwarpdir='y-' -u corrected_epi
	cd ../..
done

#Decompression de tout les RS
cd
cd documents/ImpAcq
for i in `seq -w 2 14`; do
	cd ImpAcq_${i}
	cd 12-func_task-rest
	if test ! -e corrected_epi.nii; then
		gzip -d corrected_epi.nii.gz
	fi
	cd ../..
done

#binarisation pour mask
cd
cd documents/ImpAcq
for i in `seq -w 3 11`; do
	cd ImpAcq_${i}

	cd 03-anat_T1w
	if test ! -e betbrain_mask; then
		fslmaths betbrain -bin betbrain_mask
	fi
	cd ../..
done

cd
cd documents/ImpAcq
for i in `seq -w 3 8`; do
	cd ImpAcq_0${i}

	cd 03-anat_T1w
	if test ! -e betbrain_mask; then
		fslmaths betbrain -bin betbrain_mask
	fi
	cd ../..
done

cd
cd documents/ImpAcq
for i in `seq -w 1 12`; do
	cd ImpAcq_${i}
	cd 04-func_task-anagrams_run-1
	fslsplit 04-func_task-anagrams_run-1_func_task-anagrams_run-*4.nii
	mkdir "4D Split"
	cd '4D Split'
	mv ../vol* .
	cd ../../..
done

cd
cd documents/ImpAcq
for i in `seq -w 1 12`; do
	cd ImpAcq_${i}
	cd 04-func_task-anagrams_run-1
	cd '4D Split'
	mv ../vol* .
	cd ../../..
done



python3
for i in range(9,12):
    bad_size = nib.load("/Users/pierrelechat/Documents/ImpAcq/ImpAcq_0"+str(i)+"/03-anat_T1w/betbrain_mask.nii.gz")
    good_size = nib.load("/Users/pierrelechat/Documents/ImpAcq/ImpAcq_0"+str(i)+"/04-func_task-anagrams_run-1/'4D Split'/vol0000.nii.gz")
    nib.save(nib.processing.resample_from_to(bad_size, good_size, order=1),"/Users/pierrelechat/Documents/ImpAcq/ImpAcq_0"+str(i)+"/03-anat_T1w/betbrain_mask_func1to5space.nii")


cd
cd documents/ImpAcq
for i in `seq -w 9 11`; do
	cd ImpAcq_${i}
	for j in `seq -w 1 5`; do
		cd *-func_task-anagrams_run-${j}
		fslmaths corrected_epi.nii -mas ../03-anat_T1w/betbrain_mask_func1to5space.nii func_betbrain
		cd ..
	done
	cd ..
done


#même chose pour le RS

cd
cd documents/ImpAcq
for i in `seq -w 12 14`; do
	cd ImpAcq_${i}
	cd 12-func_task-rest
	fslsplit corrected_epi.nii


	mkdir '4D Split'
	cd '4D Split'
	mv ../vol* .
	cd ../../..

done

cd
cd documents/ImpAcq
for i in `seq -w 2 11`; do
	cd ImpAcq_${i}
	cd 03-anat_T1w
	if test ! -e betbrain_mask.nii.gz; then
		fslmaths betbrain.nii.gz -bin betbrain_mask
	fi
	cd ../..
done

cd
cd documents/ImpAcq
for i in `seq -w 12 14`; do
	cd ImpAcq_${i}
	cd 12-func_task-rest
	fslmaths corrected_epi.nii -mas ../03-anat_T1w/betbrain_mask_func1to5space_RS.nii func_betbrain
	cd ../..
done

#Analyse RS



#Rangement de tous les dicoms + conversion dicom to nifti
cd
cd Documents/ImpAcq
for i in `seq -w 1 11`; do
	cd ImpAcq_${i}
	for j in `seq -w 1 15`; do
		cd ${j}-*
		if test ! -e Dicoms; then
			cd ..
			dcm2niix ${j}-*

		fi
		cd ${j}-*

		if test ! -e Dicoms; then
			mkdir Dicoms
			cd Dicoms
			mv ../MR* .
			cd ..
		fi
		cd ..
	done
	cd ..
done

cd Documents/ImpAcq
for i in `seq -w 2 9`; do
	cd ImpAcq_${i}
	cd 04-func_task-anagrams_run-1
	if test ! -e "4D split corrected"; then
		fslsplit corrected_epi.nii
		mkdir "4D split corrected"
		cd "4D split corrected"
		mv ../vol* .
		cd ..
	fi
	cd ../..
done

cd
cd Documents/ImpAcq
for i in `seq -w 2 9`; do
	cd ImpAcq_${i}
	cd 04-func_task-anagrams_run-1
	if test ! -e "4D split corrected"; then
		fslsplit corrected_epi.nii
		mkdir "4D split corrected"
		cd "4D split corrected"
		mv ../vol* .
		cd ..

	for j in `seq -w 4 8`; do
		cd 0${j}-*
		fslmaths 0${i}*.nii -mas betbrain_mask_func1to5space.nii func_betbrain
		cd ..
	cd ..
done



fugue -i 04-func_task-anagrams_run-1_func_task-anagrams_run-1_20230616153524_4.nii --dwell=0.0000026 --loadfmap=fmap_rads.nii.gz --unwarpdir y- -u result1

#dcm2niix

dcm2niix 03-anat_T1w
dcm2niix 04-func_task-anagrams_run-1
dcm2niix 05-func_task-anagrams_run-2
dcm2niix 06-func_task-anagrams_run-3
dcm2niix 07-func_task-anagrams_run-4
dcm2niix 08-func_task-anagrams_run-5
dcm2niix 10-gre_field_mapping
dcm2niix 09-gre_field_mapping
dcm2niix 13-gre_field_mapping
dcm2niix 14-gre_field_mapping
dcm2niix 12-func_task-rest


#Script pour full analyse

#!/bin/bash

# Generate the subject list to make modifying this script
# to run just a subset of subjects easier.
cd
cd Documents/ImpAcq/ImpAcq_04
for i in `seq -w 1 5` ; do
	cd *-${i}
	cp ../04-func_task-anagrams_run-1/Design_feat/Design_feat.fsf .
    sed -i '' "s|run-1|run-${i}|g" \
        Design_feat.fsf
    sed -i '' "s|run_1|run_${i}|g" \
        Design_feat.fsf


    echo "===> Starting feat for run 1"
    feat Design_feat.fsf
    cd ..
done

cd
cd Documents/ImpAcq/ImpAcq_08
cp ../ImpAcq_04/04-func_task-anagrams_run-1/Design_feat/Design_feat.fsf .
for i in `seq -w 1 5` ; do
	cd *-${i}
	cp ../Design_feat.fsf .
    sed -i '' "s|run-1|run-${i}|g" \
        Design_feat.fsf
    sed -i '' "s|run_1|run_${i}|g" \
        Design_feat.fsf

    sed -i '' "s|ImpAcq_04/Event/drive-download-20230707T150541Z-001|ImpAcq_08|g" \
        Design_feat.fsf


    echo "===> Starting feat for run 1"
    feat Design_feat.fsf
    cd ..
done


#Correction APPA

cd
cd Documents/ImpAcq
for i in `seq -w 4 11` ; do
	cd ImpAcq_${i}
	mkdir APPA_correction
	cd APPA_correction
	cp ../04-func_task-anagrams_run-1/04-func_task-anagrams_run-1_func_task-anagrams_run-1_*4.nii .
	fslsplit 04-func_task-anagrams_run-1_func_task-anagrams_run-1_*4.nii
	mkdir 4d_split_func
	cd 4d_split_func
	mv ../vol* .
	cd ..
	cp ../11-func_task-anagrams_PA/11-func_task-anagrams_PA_func_task-anagrams_PA*11.nii .
	fslsplit 11-func_task-anagrams_PA_func_task-anagrams_PA*11.nii
	mkdir 4d_split_PA
	cd 4d_split_PA
	mv ../vol* .
	cd ..

	fslmerge -t EPI_func_PA_merge 4d_split_func/vol0000.nii.gz 4d_split_func/vol0001.nii.gz 4d_split_func/vol0002.nii.gz 4d_split_PA/vol0000.nii.gz 4d_split_PA/vol0001.nii.gz 4d_split_PA/vol0002.nii.gz
	cp ../../ImpAcq_02/APPA_correction/acquistion_param.csv .
	topup --imain=EPI_func_PA_merge.nii --datain=acquistion_param.csv --out=topup_result
	cd ../..

done




applytopup --imain=vol0000_func.nii.gz,vol0000_PA.nii.gz --inindex=1,2 --datain=acquistion_param.csv --topup=topup_result --out=my_hifi_images



topup --imain=vol0000_merge.nii.gz --datain=acquistion_param.csv --out=topup_result

topup --imain=EPI_func_PA_merge.nii --datain=acquistion_param.csv --out=topup_result


cluster -i zstat1.nii.gz -t 1.5 -o cluster_index --osize=cluster_size > cluster_info.txt

#Cluster p-value correction : calculation of the smoothness estimate

smoothest -z zstat1.nii -m mask.nii.gz
DLH 0.0802583
VOLUME 164116
RESELS 57.5226
FWHMvoxel 3.63218 4.01812 3.94138
FWHMmm 7.26436 8.03625 7.88275

cluster -i zstat1.nii.gz -t 2.3 -o cluster_index --osize=cluster_size_tr_2.3 > cluster_info_tr2.3.txt
cluster -i zstat2 -t 2.3 -p 0.05 -d 0.8 --volume=164116 > cluster_zstat1.txt --osize=cluster_size_tr

#Task_RS in test group
smoothest -z zstat3.nii -m mask.nii.gz
DLH 0.00854091
VOLUME 154745
RESELS 540.535
FWHMvoxel 8.56073 8.68532 7.26988
FWHMmm 17.1215 17.3706 14.5398


cluster -i zstat1.nii.gz -t 2.3 --osize=cluster_size_tr_2.3 > cluster_info_tr2.3.txt
8. -p 0.01 -d 8.54091 --volume=154745
#merge_task_RS_test-Ctrl
DLH 0.0696299
VOLUME 154745
RESELS 66.3029
FWHMvoxel 4.24514 4.27185 3.65615
FWHMmm 8.49028 8.54371 7.31231

#AFNI

3dFWHMx -mask mask.nii.gz -input res4d.nii.gz -acf
res :
 0  0  0    0
 0.431607  4.28026  10.0784    11.4145

3dClustSim -mask mask.nii.gz -acf  0.431607  4.28026  10.0784  -athr 0.05 -pthr 0.001
# CLUSTER SIZE THRESHOLD(pthr,alpha) in Voxels
# -NN 3  | alpha = Prob(Cluster >= given size)
#  pthr  | .05000
# ------ | ------
 0.001000    88.4
# CLUSTER SIZE THRESHOLD(pthr,alpha) in Voxels
# -NN 1  | alpha = Prob(Cluster >= given size)
#  pthr  | .05000
# ------ | ------
 0.001000    64.9



#Analyse du resting state :

#Création du fichier temporel : moyenne du signal sur une ROI donnée

fslmeants -i func_betbrain_mni_space.nii.gz -o sub-02_mPFC.txt -m mPFC_reshape_trh_0.7_bin.nii.gz

fslmeants -i func_betbrain_copy.nii.gz -o sub-04_drn_activ.txt -m mask_resize.nii.gz

#Création du fichier temporel : moyenne du signal sur une ROI donnée sur tous les sujets

cd
cd Documents/ImpAcq
for i in `seq -w 3 11` ; do
	cd ImpAcq_${i}*/12-func_task-rest
	cp ../../ImpAcq_02/12-func_task-rest/Design_prepro/Design_prepro.fsf .

	sed -i '' "s|ààà|${i}|g" \
        Design_prepro.fsf
	echo 1.1
	feat Design_prepro.fsf
	if test -e Prepro_1.feat/reg/example_func2standard.mat; then
			flirt -in func_betbrain.nii.gz -ref ../../../standard/MNI152_T1_2mm_brain.nii.gz -out func_betbrain_mni_space.nii.gz -init Prepro_1.feat/reg/example_func2standard.mat -applyxfm
	else
		echo 1
		break
	fi
	mkdir Split_4D_mni_space
	if test -e func_betbrain_mni_space.nii.gz; then
		fslsplit func_betbrain_mni_space.nii.gz
	else
		echo 2
	fi

	cd Split_4D_mni_space
	mv ../vol* .
	cd ..
	if test ! -e DMN_resample; then
		mkdir DMN_resample
	fi

	cd DMN_resample
	cp ../../../resample.py .
	cd ../../..

done

python3 resample.py


cd
cd Documents/ImpAcq
for i in `seq -w 1 12` ; do
	cd ImpAcq_${i}*/12-func_task-rest/DMN_resample

	fslmaths mPFC_reshape.nii.gz -thr 60 mPFC_reshape_tr_0.6.nii.gz
	fslmaths AngularGyrus_reshape.nii.gz -thr 60 AngularGyrus_reshape_tr_0.6.nii.gz
	fslmaths PCC_reshape.nii.gz -thr 60 PCC_reshape_tr_0.6.nii.gz

	fslmaths mPFC_reshape_tr_0.6.nii.gz -bin mPFC_reshape_tr_0.6_bin.nii.gz
	fslmaths AngularGyrus_reshape_tr_0.6.nii.gz -bin AngularGyrus_reshape_tr_0.6_bin.nii.gz
	fslmaths PCC_reshape_tr_0.6.nii.gz -bin PCC_reshape_tr_0.6_bin.nii.gz

	cd ..

	mkdir Mean_signal_ROI
	cd Mean_signal_ROI
	fslmeants -i ../func_betbrain_mni_space.nii.gz -o sub-${i}_mPFC.txt -m ../DMN_resample/mPFC_reshape_tr_0.6_bin.nii.gz
	fslmeants -i ../func_betbrain_mni_space.nii.gz -o sub-${i}_AngularGyrus.txt -m ../DMN_resample/AngularGyrus_reshape_tr_0.6_resamp_bin.nii.gz
	fslmeants -i ../func_betbrain_mni_space.nii.gz -o sub-${i}_PCC.txt -m ../DMN_resample/PCC_reshape_tr_0.6_bin.nii.gz
	cd ../../..

done

fslmaths AngularGyrus_reshape_tr_0.6_resamp.nii.gz -bin AngularGyrus_reshape_tr_0.6_resamp_bin.nii.gz
fslmaths mPFC_reshape_tr_0.6_resamp.nii.gz -bin mPFC_reshape_reshape_tr_0.6_resamp_bin.nii.gz
fslmaths PCC_reshape_tr_0.6_resamp.nii.gz -bin PCC_reshape_tr_0.6_resamp_bin.nii.gz

fslmeants -i ../func_betbrain_mni.nii.gz -o sub-14_mPFC.txt -m ../DMN_resample/mPFC_reshape_tr_0.6_resamp_bin.nii.gz
fslmeants -i ../func_betbrain_mni.nii.gz -o sub-14_AngularGyrus.txt -m ../DMN_resample/AngularGyrus_reshape_tr_0.6_resamp_bin.nii.gz
fslmeants -i ../func_betbrain_mni.nii.gz -o sub-14_PCC.txt -m ../DMN_resample/PCC_reshape_tr_0.6_resamp_bin.nii.gz

cd
cd Documents/ImpAcq
for i in `seq -w 1 12` ; do
	cd ImpAcq_${i}*/12-func_task-rest/DMN_resample

	fslmaths mPFC_reshape.nii.gz -thr 60 mPFC_reshape_tr_0.6.nii.gz
	fslmaths AngularGyrus_reshape.nii.gz -thr 60 AngularGyrus_reshape_tr_0.6.nii.gz
	fslmaths PCC_reshape.nii.gz -thr 60 PCC_reshape_tr_0.6.nii.gz

	fslmaths mPFC_reshape_tr_0.6.nii.gz -bin mPFC_reshape_tr_0.6_bin.nii.gz
	fslmaths AngularGyrus_reshape_tr_0.6.nii.gz -bin AngularGyrus_reshape_tr_0.6_bin.nii.gz
	fslmaths PCC_reshape_tr_0.6.nii.gz -bin PCC_reshape_tr_0.6_bin.nii.gz

	cd ..

	mkdir Mean_signal_ROI
	cd Mean_signal_ROI
	fslmeants -i ../func_betbrain_mni_space.nii.gz -o sub-${i}_mPFC.txt -m ../DMN_resample/mPFC_reshape_tr_0.6_bin.nii.gz
	fslmeants -i ../func_betbrain_mni_space.nii.gz -o sub-${i}_AngularGyrus.txt -m ../DMN_resample/AngularGyrus_reshape_tr_0.6_bin.nii.gz
	fslmeants -i ../func_betbrain_mni_space.nii.gz -o sub-${i}_PCC.txt -m ../DMN_resample/PCC_reshape_tr_0.6_bin.nii.gz
	cd ../../..

done

fslmeants -i func_betbrain_mni.nii.gz -o sub-12_PCC.txt -m DMN_resample/PCC_reshape_tr_0.6_bin.nii.gz


cd
cd Documents/ImpAcq
for i in `seq -w 4 11` ; do
	cd ImpAcq_${i}*/12-func_task-rest/
	mkdir Design_first_analyses
	cd Design_first_analyses
	cp ../../../ImpAcq_03/12-func_task-rest/Design_first_analyses/Design_first_analyses.fsf .
	sed -i '' "s|ààà|${i}|g" \
        Design_first_analyses.fsf
	feat Design_first_analyses.fsf

	cd ../../..

done

#Première étape combinaison RS et Task : création dossier, importation fichier
cd
cd Documents/ImpAcq
for i in `seq -w 1 11` ; do
	cd ImpAcq_${i}*
	mkdir Task_RS_combined
	cd Task_RS_combined



	for i in `seq 1 5`; do
		cp ../*anagrams*-${i}/func_betbrain.nii.gz func_betbrain_${i}.nii.gz
	done

	mkdir vol_Task

	fslsplit func_betbrain_1.nii.gz

	cd vol_Task
	mv ../vol* .
	cd ..
	pwd
	cp ../*task-rest*/func_betbrain_mni_space.nii.gz rs_mni_space.nii.gz

	fslsplit rs_mni_space.nii.gz
	mkdir vol_rs
	cd vol_rs
	pwd
	mv ../vol* .

	cd ..
	mv vol_rs/vol_Task .
	cd ../..

done

#Utilisation de fsleyes pour placer func_betbrain dans MNI et merge des task_mni
cd
cd Documents/ImpAcq
for i in `seq -w 2 11` ; do
	cd ImpAcq_${i}*
	cd Task_RS_combined
	cp ../*anagrams*/Analyse_FvsNF.feat/reg/example_func2standard.mat .
	cp ../*anagrams*/Analyse_Found.feat/reg/example_func2standard.mat .
	cp ../*anagrams*/Analyse_FvsNF.feat/reg/standard.nii.gz .
	cp ../*anagrams*/Analyse_Found.feat/reg/standard.nii.gz .
	if test -e example_func2standard.mat ; then
		flirt -in func_betbrain_1.nii.gz -ref standard.nii.gz -applyxfm -init example_func2standard.mat -out  func_betbrain_std_1.nii.gz
		flirt -in func_betbrain_2.nii.gz -ref standard.nii.gz -applyxfm -init example_func2standard.mat -out  func_betbrain_std_2.nii.gz
		flirt -in func_betbrain_3.nii.gz -ref standard.nii.gz -applyxfm -init example_func2standard.mat -out  func_betbrain_std_3.nii.gz
		flirt -in func_betbrain_4.nii.gz -ref standard.nii.gz -applyxfm -init example_func2standard.mat -out  func_betbrain_std_4.nii.gz
		flirt -in func_betbrain_5.nii.gz -ref standard.nii.gz -applyxfm -init example_func2standard.mat -out  func_betbrain_std_5.nii.gz
	fi
	fslmerge -t func_merge_std func_betbrain_std_*
	cd ../..
done

cd
cd Documents/ImpAcq
for i in `seq -w 2 11` ; do
	cd ImpAcq_${i}*
	cd Task_RS_combined


	rm -r vol_Task
	mkdir vol_Task
	fslsplit func_betbrain_std_1.nii.gz
	cd vol_Task
	mv ../vol* .

	cd ..
	mv vol_Task/vol_rs .
	cd ../..

done
#Script python pour mettre le RS et les func dans le même header
#Script pour creer le merged RS_resamp

cd
cd Documents/ImpAcq
for i in `seq -w 2 9` ; do
	cd ImpAcq_0${i}*/Task_RS_combined/vol_rs
	fslmerge -t RS_resamp_merge RS_resamp*
	cd ../../..
done
#Script suppression des dossiers Task_RS
cd
cd Documents/ImpAcq
for i in `seq -w 1 11` ; do
	cd ImpAcq_${i}*
	rm -r Task_RS_combined


	cd ..
done


#Script pour creer le merged Task +rs
cd
cd Documents/ImpAcq
for i in `seq -w 2 9` ; do
	cd ImpAcq_0${i}*/Task_RS_combined
	cp vol_rs/RS_resamp_merge.nii.gz .
	fslmerge -t merge_task_rs_mni func_merge_std.nii.gz RS_resamp_merge.nii.gz
	cd ../..
done





