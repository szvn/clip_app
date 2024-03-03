import SwiftUI

struct ContentView: View {
    @State private var selectedImage: UIImage?
    @State private var isShowingImagePicker = false
    @State private var textFields: [String] = []
    @State private var textFieldInput: String = ""
    @State private var baseURLString = "http://192.168.2.42:5000" // Adjust port number as per your server
    
    var body: some View {
        VStack {
            if let image = selectedImage {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .padding()
            } else {
                Text("No Image Selected")
                    .padding()
            }
            
            Button(action: {
                self.isShowingImagePicker.toggle()
            }) {
                Text("Select Image")
            }
            
            ForEach(0..<textFields.count, id: \.self) { index in
                TextField("Enter text", text: self.$textFields[index])
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
            }
            
            Button(action: {
                self.textFields.append(self.textFieldInput)
                self.textFieldInput = ""
            }) {
                Text("Add Text Field")
            }
            
            Button(action: {
                if let image = self.selectedImage {
                    if let base64String = image.jpegData(compressionQuality: 1.0)?.base64EncodedString() {
                        let json: [String: Any] = [
                            "images": [base64String],
                            "labels": self.textFields
                        ]
                        
                        if let jsonData = try? JSONSerialization.data(withJSONObject: json) {
                            if let jsonString = String(data: jsonData, encoding: .utf8) {
                                //print(jsonString)
                                sendHTTPRequest(jsonString: jsonString)
                            }
                        }
                    }
                }
            }) {
                Text("Save All Text Fields & Image")
            }
        }
        .sheet(isPresented: $isShowingImagePicker) {
            ImagePickerView(selectedImage: self.$selectedImage, isPresented: self.$isShowingImagePicker)
        }
    }
    
    func sendHTTPRequest(jsonString: String) {
        guard let url = URL(string: baseURLString) else {
            print("Invalid URL")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = jsonString.data(using: .utf8)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error.localizedDescription)")
                return
            }
            
            if let data = data, let responseString = String(data: data, encoding: .utf8) {
                print("Response: \(responseString)")
            }
        }
        
        task.resume()
    }
}

struct ImagePickerView: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    @Binding var isPresented: Bool
    
    func makeCoordinator() -> Coordinator {
        return Coordinator(parent: self)
    }
    
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let imagePicker = UIImagePickerController()
        imagePicker.delegate = context.coordinator
        imagePicker.sourceType = .photoLibrary
        return imagePicker
    }
    
    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {
        // No update needed
    }
    
    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: ImagePickerView
        
        init(parent: ImagePickerView) {
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.selectedImage = image
            }
            
            parent.isPresented = false
        }
        
        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.isPresented = false
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

