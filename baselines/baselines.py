def baselines(ami_or_icsi, asr_or_human_1, asr_or_human_2):  
    
    import os
    import re
    import csv
    
    # I modified the source files so that the system uses our custom list of stopwords
    from summa import summarizer # https://github.com/summanlp/textrank
    
    path_root = 'C:\\Users\\mvazirg\\Documents\\text_stream_topic_detection_most_recent\\'
    
    path = path_root + 'code\\overall_summary_modules\\Python\\baselines\\ClusterRank_baseline'
    os.chdir(path)
    import functions_ClusterRank_high
    
    # parameters for the ClusterRank function
    # the stopwords are always the same (corpus-independent)
    path_name_stopwords = path_root + 'data\\output\\ami\\custom_stopwords.csv'
    # like in Garg et al. (2009)
    sim_threshold, window_threshold = 0.06, 3
    
    # read names of the test set meetings
    my_path = path_root + '\\data\\output\\' + ami_or_icsi + '\\'
    test_set_names = list()
    with open(my_path + 'names_meetings_test_set.csv', 'r+') as csvfile:
         rows = csv.reader(csvfile, delimiter=' ')
         for row in rows:
             test_set_names.append(row)
    
    test_set_names = [item for sublist in test_set_names for item in sublist]
    test_set_names = test_set_names[1:len(test_set_names)]
    
    # read max_lengthes of the summaries as determined by the linear regression model
    my_path = path_root + '\\data\\output\\' + ami_or_icsi + '\\'
    max_lengthes = list()
    with open(my_path + 'max_summary_lengthes_test_set.csv', 'r+') as csvfile:
         rows = csv.reader(csvfile, delimiter=' ')
         for row in rows:
             max_lengthes.append(row)
    
    max_lengthes = [item for sublist in max_lengthes for item in sublist]
    max_lengthes = max_lengthes[1:len(max_lengthes)]
    
    # read custom stopwords
    my_path = path_root + '\\data\\output\\'
    custom_stopwords = list()
    with open(my_path + 'custom_stopwords.csv', 'r+') as csvfile:
         rows = csv.reader(csvfile, delimiter=' ')
         for row in rows:
             custom_stopwords.append(row)
    
    custom_stopwords = [item for sublist in custom_stopwords for item in sublist]
    custom_stopwords = custom_stopwords[1:len(custom_stopwords)]
    
    k = 0
    
    for name in test_set_names:
        
        # read raw text
        filename = name + '_full_raw_text' + asr_or_human_1 + '.txt'
        
        my_path = path_root + '\\data\\output\\'+ ami_or_icsi +'\\text_for_baselines\\'
        with open(my_path + filename, 'r+') as txtfile:
            raw_text = txtfile.read()
       
        # remove formatting
        raw_text =  re.sub("\s+", " ", raw_text)
        
        utterances = raw_text.split('.')
        # to remove the yeahs, oks, etc. 
        utterances = [utterance.strip().lower() for utterance in utterances if len(utterance.strip().split(' '))>1]   
        raw_text  = '. '.join(utterances)
        
        # remove the {vocalsound}'s, {disfmarker}'s, etc.
        raw_text = re.sub('{.*?}', '', raw_text)
                
        # ClusterRank baseline
        sorted_sentences = functions_ClusterRank_high.Cluster_Rank(raw_text, path_name_stopwords, sim_threshold, window_threshold)
        
        for my_max_length in [100,150,200,250,300,350,400,450,500]:
            
            # textRank baseline
            text_rank_to_write = summarizer.summarize(text = raw_text, words = my_max_length) 
            # write summary to file
            filename = name + '_' + str(my_max_length) + '-text-rank-baseline' + asr_or_human_2 + '.txt'
            my_path = path_root + '\\data\\output\\'+ ami_or_icsi +'\\summaries\\text_rank_baseline\\'
            with open(my_path + filename, 'w+') as txtfile:
                txtfile.write(text_rank_to_write)
            
            # ClusterRank sentence selection: greedily select one sentence at a time from the top until size constraint has been reached
            summary = str()
            for element in sorted_sentences:
                sentence_temp = element[1].split(' ')
                len_summ = len(summary.split(' '))
                
                if (len_summ + len(sentence_temp)) > my_max_length:
                    to_add = sentence_temp[0:(my_max_length-len_summ)]
                else:
                    to_add = sentence_temp
                
                summary = summary + ' ' + '\n' + ' '.join(to_add)
                        
                if len_summ >= (my_max_length - 1) :
                    break

            cluster_rank_to_write = summary + '.'
        
            # write ClusterRank summary
            filename = name + '_' + str(my_max_length) + '-cluster-rank-baseline' + asr_or_human_2 + '.txt'
            my_path = path_root + '\\data\\output\\'+ ami_or_icsi +'\\summaries\\cluster_rank_baseline\\'
            with open(my_path + filename, 'w+') as txtfile:
                txtfile.write(cluster_rank_to_write[2:len(cluster_rank_to_write)])
        
        print k 
        k += 1


# generate summaries

# asr_or_human_1 = c('', '_human')
# asr_or_human_2 = c('', '-human')

baselines(ami_or_icsi="icsi", asr_or_human_1="", asr_or_human_2="")


