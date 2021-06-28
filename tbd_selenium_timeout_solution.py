from lxml import etree

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
prefs = {
    'profile.default_content_setting_values': {
    'images': 2,    # 禁用图片的加载
    'javascript': 2 ##禁用js，可能会导致通过js加载的互动数抓取失效
    }
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless") # 不弹出浏览器
browser = webdriver.Chrome(options=chrome_options)
browser.implicitly_wait(5) # 操作、获取元素时的隐式等待时间
browser.set_page_load_timeout(10) # 页面加载超时等待时间
main_win = browser.current_window_handle #记录当前窗口的句柄
all_win = browser.window_handles
# 开始访问页面
print('Opening page')
urls = [] # 定义你想要抓取的全部的页面
for url in urls:
    try:
        if len(all_win) == 1:
            print('弹出保护罩')
            js = 'window.open("https://www.baidu.com");'
            browser.execute_script(js)
            # 还是定位在main_win上的
            for win in all_win:
                if main_win != win:
                    print('保护罩WIN', win, 'Main', main_win)
                    browser.switch_to.window(main_win)
        browser.get(url) # 此处访问你需要的URL
        body = browser.page_source
        html = etree.HTML(body)
    # 下面是你的抓取逻辑 省略
    except:
    # 超时
        print('Time out')
        # 切换新的浏览器窗口
        for win in all_win:
            if main_win != win:
                print('WIN', win, 'Main', main_win)
                print('切换到保护罩')
                browser.close()
                browser.switch_to.window(win)
                main_win = win
                
        js = 'window.open("https://www.baidu.com");'
        browser.execute_script(js)
        if 'time' in str(traceback.format_exc()):
            print('页面访问超时')