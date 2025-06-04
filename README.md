# polybar-weather-script
polybar 的python3 天气模块多图标

![图片](https://github.com/user-attachments/assets/e3d2c661-b086-422a-b5d5-fce29258a816)

字体选择

```ini
...
font-3="Noto Color Emoji:scale=6;4"      
...
```

modules

```ini
[module/weather]
type = custom/script
exec = $HOME/.config/polybar/scripts/weather.sh
label = %{T1}%output%%{T3} #如果无法找到Unicode 图标 则选择font-3的字体 即图标字体
interval = 600
```


