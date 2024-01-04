using Microsoft.ML;
using System;

namespace Model_1_0
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Load the trained model
            var mlContext = new MLContext();
            var model = mlContext.Model.Load("Model_1.0.mlnet", out var modelSchema);

            // Save the model as ONNX
            mlContext.Model.Save(model, modelSchema, "Model_1.0.onnx");
        }
    }
}