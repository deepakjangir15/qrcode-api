# QreativeQR: A Customizable QR Code Generator API Documentation

The QR code generator API is a powerful tool that allows users to generate custom QR codes with ease. With this API, you can create a simple QR code, customize the size, border size, and color of the QR code, set the background color, and even insert an image or logo in between the QR code. The image can be a base64 image or uploaded via a POST request. With these powerful features, this API provides users with the flexibility they need to create custom QR codes that match their brand or application’s design.

### Three endpoints:
1. Generate Simple QR Code - GET
The simple QR code generator endpoint allows users to easily create a QR code by passing in the data that they want to convert. With this endpoint, you can customize the size and border spacing of the generated QR code. Additionally, users can choose whether to force download the QR code file or not.

Parameters:

- QR_data: (required) The data to be converted to QR code. This can be any text or URL that you want to encode into a QR code.
- QR_size: (optional) The size of the QR code. By default, the API will generate a QR code with a size of 10 (250 x 250). However, you can modify this parameter to set the size of your choice.
- spacing: (optional) The border spacing of the QR code. By default, the API will generate a QR code with a border spacing of 4 pixels. However, you can modify this parameter to adjust the border spacing according to your needs.
- download_file: (optional) A boolean parameter that determines whether the user wants to force download the QR code file or not. If set to 1, the API will return the QR code file as an attachment, prompting the user to download it. If set to 0, the QR code file will be returned as a response.

2. Generate Colored QR Code - GET
This endpoint generates a colored QR code for the given data. The endpoint takes in the following parameters:

- QR_data: the data to be encoded into the QR code.
- qrcolor (optional): the color of the QR code. The default color is black.
- bgcolor (optional): the background color of the QR code. The default color is white.
- QR_size (optional): the size of the QR code.
- spacing (optional): the border space of the QR code.
- download_file (optional): determines whether the user wants to force download the QR code.

Using this endpoint, developers can generate a colored QR code for their data with customizations such as color, size, and border spacing. The ability to modify the color and background color of the QR code provides developers with the flexibility to match the QR code to their branding.

3. Generate custom QR Code with Logo/Image - POST
This endpoint generates a custom-colored QR code with an embedded image/logo. The endpoint takes in the following parameters:

- QR_data: the data to be encoded into the QR code.
- base64_image: the base64 format of the image/logo to be embedded in the QR code.
- circular_logo (optional): determines whether the embedded logo should be circular or square.
- qrcolor (optional): the color of the QR code. The default color is black.
- bgcolor (optional): the background color of the QR code. The default color is white.
- QR_size (optional): the size of the QR code.
- spacing (optional): the border space of the QR code.
- download_file (optional): determines whether the user wants to force download the QR code.

Using this endpoint, developers can generate a custom-colored QR code with an embedded image/logo. The embedded

 logo can be circular or square, providing developers with the flexibility to match the QR code to their branding. Additionally, the ability to modify the color and background color of the QR code allows developers to create a fully customized QR code.

# QreativeQR: A Customizable QR Code Generator Overview

The QR code generator API provides developers with the ability to create custom QR codes for their applications. With this API, developers can customize various aspects of the QR code, including its size, border spacing, color, and background color. The API also allows developers to insert images or logos within the QR code, and these images can be uploaded as base64-encoded images or via a POST request.

By providing these customization options, the API enables users to create QR codes that are consistent with their brand identity, making it easier to incorporate QR codes into their marketing and advertising campaigns. The ability to insert images or logos into the QR code also provides developers with the opportunity to provide additional context or branding to the user.

Overall, the QR code generator API provides developers with a powerful tool that allows them to create custom QR codes that match their brand’s identity and seamlessly integrate them into their applications.
