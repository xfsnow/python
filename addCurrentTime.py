# 在 Sublime Text 3 中配置快捷键插入当前时间值，点击菜单栏中 Preferences -> Browser Packages...
# 会弹出资源管理器，进入 User 文件，新建一个名为 addCurrentTime.py 的文件，添加以下文件的内容：
import datetime
import sublime_plugin

class AddCurrentTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet",
            {
                "contents": "%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

# 在 Sublime Text 3 的菜单栏中点击 Preferences -> Key Bindings
# 在弹出窗口右边栏添加以下内容：
# [
#     { "keys": ["ctrl+f5", "ctrl+f5"], "command": "add_current_time" }
# ]
# 在文件中连续按 2 次 Ctrl+F5 就可以插入形如 2024-07-09 18:54:43 的时间值了。