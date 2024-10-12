
export setting_file=../generate_setting.json
cd Generation

for i in {1..2}
do
    python datagen.py --generate_setting $setting_file
    # python datagen_simplefewshot.py --generate_setting $setting_file
done