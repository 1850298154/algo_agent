from src.ui.file_upload import (
    files_model,
    files_store,
)
from src.utils.path_util import static_path

def get_input_file_prompt():
    input_file_prompt = f"""
{
    "\n\n上传的数据是："
    + "；".join(["文件名："+file.name 
                + "，文件大小：" + str(file.size) + " 字节，" 
                + "文件类型：" + file.type 
                for file in files_model.uploaded_files]) 
    + "。\n\n"
    if files_model.uploaded_files 
    else ""
}
{
    "上传数据的目录、" if files_model.uploaded_files else ""
}
{
    "执行python代码的启动路径和程序运行输出的工作路径都是："
    +static_path.Dir.UPLOAD_DIR.resolve().as_posix()
}
"""
    # input_file_prompt = ("\n\n上传的数据是："+
    #             "；".join(["文件名："+file.name + 
    #                 "，文件大小：" + str(file.size) + " 字节，" + 
    #                 "文件类型：" + file.type 
    #                 for file in files_model.uploaded_files]) + 
    #             "。\n上传数据的目录、执行python代码的启动路径和程序运行输出的工作路径都是："+static_path.Dir.UPLOAD_DIR.resolve().as_posix())
    return input_file_prompt