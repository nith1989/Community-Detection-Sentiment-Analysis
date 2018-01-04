"""
sumarize.py
"""
def main():
    collect = open("Collection Summary.txt",'r',encoding='utf8').readlines()
    cluster =  open("Clustering Summary.txt",'r',encoding='utf8').readlines()
    classify = open("Classification Summary.txt",'r',encoding='utf8').readlines()
    file = open("summary.txt","w",encoding='utf8')
    file.writelines(collect)
    file.writelines(cluster)
    file.writelines(classify)
    file.close()

if __name__ == '__main__':
    main()
