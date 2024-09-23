from flet import *
import requests
import os
import io
from PIL import Image as Img


HF_TOKEN='' # you must have a Hugging face api key

# you can change the modle in API_URL 
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

headers = {"Authorization": "Bearer "+HF_TOKEN}

# you can change the  folder  that will contain all the genrated images  
folder_dir= "assets/images"

def getimage(text_image):
        
        
        
        def query(payload):
           response = requests.post(API_URL, headers=headers, json=payload)
           return response.content
       
    
        image_bytes = query({
            
        
          "inputs":f"{text_image}",
        })
        #You can access the image with PIL.Image 
        
        image = Img.open(io.BytesIO(image_bytes))
        
        
    
       # iterate through saved images just to give an id to the new  genrated image ## 
        image_id=0
        for images in os.listdir(folder_dir):
            if (images.endswith(".jpg")):
               image_id +=1        
                
        path_new_image=f"{folder_dir}/image-{image_id}.jpg"  
        image.save(path_new_image)
        return path_new_image
        
        

      
            
        
      
   
 
        

        
        



def main(page: Page):
   
    page.title='Generate images'
 
    page.window.height=740
    page.window.width=480
    page.theme_mode=ThemeMode.LIGHT
    page.theme=Theme()

    page.bgcolor=colors.LIGHT_BLUE_ACCENT_700
    all_images =Row(wrap=False,height=250, scroll="always") 
    id_range=TextField(label="Id...",width=60,height=40,text_size=12)
    
   
                            
      
        
        
        

    def  update_images():
       
       
        all_images.controls.clear()
        
        for i,image in enumerate(os.listdir(folder_dir)):
        
            all_images.controls.append(
              Card(
            
                content=Container(
            
                    
                       Stack(
                        [Image(
                          
                          src=f"images/{image}",
                          width=200,
                          height=200,
                          fit=ImageFit.COVER,
                          repeat=ImageRepeat.NO_REPEAT,
                          border_radius=border_radius.all(10),
                
                           ),
                          TextButton(f"{i}",width=40,style=ButtonStyle(enable_feedback=True)),
                          
                           
                        ]),
                        
                    
                ),
                
                
               )
            ) 
        page.update()
   
    update_images()
    
    def Deleteoneimg(e):
            if id_range.value != '':
                
              for index,image in enumerate(os.listdir(folder_dir)):
                if (image.endswith(".jpg")) and index == int(id_range.value):
                
                    os.remove(folder_dir+"/"+image)
                    update_images()
                   
                    break    
            else :
                id_range.value="filed are Empty"
                
                
                
    def clear_all_images(e):
   
            for image in os.listdir(folder_dir):
                if (image.endswith(".jpg")):
                   os.remove(folder_dir+"/"+image)  
                   update_images()
                 
                   
           
    
    def handle_close(e):
        page.close(dlg_modal)
   
   
    dlg_modal = AlertDialog(
        modal=True,
        
        title=Text("Information"),
        content=Text("Generate image apps utilize artificial intelligence to create unique images from text prompts"),
        actions=[
            TextButton("close", on_click=handle_close),
          
        ],
        actions_alignment=MainAxisAlignment.END,
       
    )

    page.appbar = AppBar(
      
        leading_width=40,
        title=Text("Main"),
        center_title=False,
        bgcolor=colors.BLUE_700,
        actions=[
        
            IconButton(icons.FILTER_3),
            PopupMenuButton(
                items=[
                    PopupMenuItem(text="Menu"),
                    PopupMenuItem() ,# divider
                   
                    PopupMenuItem(
                        content=ElevatedButton("Delete all images",icon=icons.CLEAR,width=200, on_click=clear_all_images,
                        style=ButtonStyle(shape={ControlState.DEFAULT: RoundedRectangleBorder(radius=0)}),
                    )),
                    PopupMenuItem(
                        content=Row([
                          id_range,
                          ElevatedButton("DELETE",icon=icons.DELETE,width=129, on_click=Deleteoneimg,style=ButtonStyle(shape={ControlState.DEFAULT: RoundedRectangleBorder(radius=0)}))
                        ])
                    ),
                    PopupMenuItem(
                       padding=0,
                       content=ElevatedButton("Open Info",icon=icons.INFO,width=200,style=ButtonStyle(
                         
                            shape={
                            
                             ControlState.DEFAULT: RoundedRectangleBorder(radius=0),
                            }
                           ), on_click=lambda e: page.open(dlg_modal)
                    )),
                   
                ]
            ),
        ],
    )
   
    
 
    image_path='#'
    def asyntext(e):
        if tinput.value =='':
            tinput.value ="feild empty"
        
        else :
            
            image_path=getimage(tinput.value)
            timage.src =image_path
            tinput.value=''
            update_images()
            page.update()  
    
    

    
    
    tinput=TextField(
        label='image description',
        icon=icons.IMAGE,
        height=43,
        width=400,
        
        
    )
    timage=Image(src="images/image-3.jpg",fit=ImageFit.COVER,border_radius=8)
    page.add(
        
        Container(
                  content=Row([      
                        tinput,
                        IconButton(
                                                        icon=icons.SEND_ROUNDED,
                                                        tooltip="Send message",
                                                        on_click=asyntext,
                        ),   
                ],alignment=MainAxisAlignment.CENTER),
                    margin=0,
                    padding=10,
                    alignment=alignment.center,
                    bgcolor=colors.BLUE_200,
                  
                    border_radius=10,      
                        
                  
        ) , 
        dlg_modal,
        
        Column([
           
           
           Container(
                    content=timage,
                    margin=10,
                    padding=10,
                    alignment=alignment.center,
                    bgcolor=colors.BLUE_200,
                    
                    expand=True,
                    border_radius=10,
            ),  
            
            
            
        ],horizontal_alignment=CrossAxisAlignment.CENTER,spacing=40,alignment=CrossAxisAlignment.CENTER,expand=True),
      
        all_images
        
    )
    page.update()
    
   
app(main,assets_dir="assets")
