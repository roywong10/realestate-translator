import nltk
import sys

PathToEngText = sys.argv[1]  
# nltk.download()

# file = open(PathToEngText, 'r')
# lines = file.readlines()
#
# words = []
# tags = []
# for sen in lines:
#     t = nltk.word_tokenize(sen)
#     r = nltk.pos_tag(t)
#     tags.append(r)
#     ners = nltk.ne_chunk(r)
#     print('sen: ', sen, end='\n#################\n')
#     print('words: ', t,end='\n##################\n')
#     print('tags: ', r,end='\n################ner\n')
#     print('ners: ', ners,end='\n\n\n\n\n')

# print("words: ",words)

# tags = []
# for tokens in words:
#     r = nltk.pos_tag(tokens)
#     tags.append(r)
#     print(r,end='\n################ners################\n')
#     print(nltk.ne_chunk(r))



