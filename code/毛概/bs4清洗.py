import requests
from bs4 import BeautifulSoup as BS
import json

def main():
    file = open('E:/桌面/毛概/all_link.txt','w', encoding='utf-8')
    json1 = open('E:/桌面/毛概/毛概预题库.json','w+',encoding='utf-8')

    url = 'https://wlkc.ouc.edu.cn/webapps/gradebook/do/student/viewAttempts?method=list&course_id=_25851_1&outcome_definition_id=_173599_1&outcome_id=_3984061_1&takeTestContentId=_1136732_1&maxAttemptsReached=false'
    header = {
        'User-Agent': '##YOUR_USER-AGENT',
        'cookie': '##YOUR-COOKIE'
    }
    text = requests.get(url, headers=header).text


    soup = BS(text,'html.parser')
    tbody = soup.find_all('tbody')

    all = 238
    single = 81
    single_num = 0

    multiple = 79
    multiple_num = 0

    tf = 78
    tf_num = 0
    print(f'总数: {all} -- 单选: {single}, 多选: {multiple}, 判断: {tf}')

    link = []
    for tr in tbody:
        td_ = tr.find_all('a')
        for a in td_:
                a1 = str(a.get('href'))
                link.append(a1)

                file.write(str(a) + '\n')
        print(f"总页数: {len(td_)}\n总题数: {len(td_)*15}(含重复)\n")

    file.close()
    data = {}
    num = 0
    for i in link:
        num += 1

        url_i = 'https://wlkc.ouc.edu.cn' + i
        text_i = requests.get(url_i, headers=header).text
        soup_i = BS(text_i,'html.parser')

        ul = soup_i.find(id='content_listContainer')

        all_li = ul.find_all('li')
        for li in all_li:
            L = []
            div = li.select_one('.details')
            table = div.find('table')
            tr = table.find_all('tr')
            td_1 = tr[1].find_all('td')
            td_ques_pre = td_1[1].find('div')

            td_ques = td_ques_pre.text
        
            # break

            #正式
            # print('>'*70)
            # print(td_ques)
            # print('-'*70)

            td_tr_all = tr[2].find_all('tr')
            
            check_num = 0
            for i in range(0,len(td_tr_all)):
                check_tag = td_tr_all[i].find_all('td')[0].find('span')
                try:
                    check = check_tag.text
                except:
                    pass
                if check == '答案：':
                    check_num = 1


                if check_num == 0:
                    continue
                else:
                    td_text = td_tr_all[i].find_all('td')[-1]
                    div = td_text.find('div')
                    ans_all = div.find_all('span')
                    try:
                        i_text = div.find('p').text.strip()
                        # print('判断题')
                    except:
                        ans_span = ans_all[-1]
                        i_text = ans_span.find('div').text.strip()
                        # try: 
                        #     i_text = ans_span.find('label').text.strip()
                        #     single_num += 1
                        #     # print('选择题')
                        # except:
                        #     i_text = ans_span.find('div').text.strip() 
                        #     # print('选择题')

                    tf_span = ans_all[0]
                    img = tf_span.find('img')
                    if img != None:     
                        i_text += '√'
                    
                    L.append(i_text)
                    #正式
                    # print(i_text)
                    
            #正式
            # print('<'*70)
            # print('\n')

            data[td_ques] = L
            # break
        print(f'完成--{num}/{len(link)}', end='\r')
        # break

    json.dump(data,json1)
    json1.close()
    print(f'总题数: {len(data)}(降重后)')

    for i in data.keys():
        if '对' in data[i]:
            tf_num += 1
        else:
            tf_temp = 0
            for true in data[i]:
                if '√' in true:
                    tf_temp += 1

            if tf_temp == 1:
                single_num += 1
            else:
                multiple_num += 1 
            
    if len(data) != all:
        if len(data) < all:
            print('收集:     |  总数:')
            print('总数: %3d < %3d, 还剩%3d道题' %(len(data), all, all-len(data)))
            if single_num < single:
                print(f'单选: %3d < %3d, 还剩%2d道题' %(single_num,single,single-single_num))
            if multiple_num < multiple:
                print(f'多选: %3d < %3d, 还剩%2d道题' %(multiple_num,multiple,multiple-multiple_num))
            if tf_num < tf:
                print(f'判断: %3d < %3d, 还剩%2d道题' %(tf_num,tf,tf-tf_num))
        else:
            print('**出现问题**')
            if single_num > single:
                print(f'单选: {single_num} > {single}, 超出{single_num-single}道题')
            if multiple_num > multiple:
                print(f'多选: {multiple_num} > {multiple}, 超出{multiple_num-multiple}道题')
            if tf_num > tf:
                print(f'判断: {tf_num} > {tf}, 超出{tf_num-tf}道题')
    else:
        len(data) == all and single_num == single and multiple_num == multiple and tf_num == tf
        print('收集完成')

if __name__=='__main__':
    main()
