import json
for i,info in enumerate(infos):
    with open (f'D:/zyt/git_ln/algo_agent/github_tool/{i:02d}-{info.name}.json', 'w', encoding='utf-8') as f:
        f.write(info.model_dump_json(indent=4))

import json
new_infos = [i.model_dump() for i in infos]
with open (f'D:/zyt/git_ln/algo_agent/github_tool.json', 'w', encoding='utf-8') as f:
    json.dump (new_infos, f, ensure_ascii=False, indent=4)






