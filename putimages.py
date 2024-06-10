import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[('image1.jpg','Elon Musk'),
      ('image3.jpg','Bill Gates'),
      ('image5.jpg','Sundar Pichai'),
      ('image7.jpg','Mukesh Ambani'),
      ('image8.jpg','Ratan Tata')
      ]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('famousentrepreneur-images','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})