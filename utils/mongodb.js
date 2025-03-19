const mongoose = require('mongoose');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Mongoose connection function
async function connectToMongoose() {
  const uri = process.env.MONGODB_URI;
  if (!uri) {
    throw new Error('MongoDB URI is not defined in environment variables');
  }

  try {
    await mongoose.connect(uri, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
    console.log('Successfully connected to MongoDB with Mongoose');
  } catch (error) {
    console.error('MongoDB connection error:', error);
    throw error;
  }
}

// Function to save results using Mongoose with explicit collection
async function saveToMongoDB(data) {
  try {
    await connectToMongoose();
    
    // Get database and collection names from environment variables
    const dbName = process.env.MONGODB_DB_NAME;
    const collectionName = process.env.MONGODB_COLLECTION_NAME;
    
    if (!dbName || !collectionName) {
      throw new Error('MongoDB database or collection name is not defined in environment variables');
    }
    
    // Define schema and model with explicit collection name
    const predictionSchema = new mongoose.Schema({
      symbol: String,
      startDate: String,
      endDate: String,
      timespan: String,
      mse: Number,
      rmse: Number,
      mae: Number,
      accuracy: Number,
      predictions: Array,
      created_at: {
        type: Date,
        default: Date.now
      }
    }, { collection: collectionName });  // Explicitly set collection name

    // Use the current connection but specify the DB name
    const conn = mongoose.connection.useDb(dbName);
    
    // Create the model with the connection
    const PredictionModel = conn.model('Prediction', predictionSchema);
    
    // Add timestamp if not present
    const documentToInsert = {
      ...data,
      created_at: new Date(),
    };
    
    const predictionData = new PredictionModel(documentToInsert);
    const result = await predictionData.save();
    
    console.log(`Successfully saved prediction to MongoDB collection '${collectionName}' with id: ${result._id}`);
    return result;
  } catch (error) {
    console.error('Error saving to MongoDB:', error);
    throw error;
  } finally {
    // Close the connection after saving
    await mongoose.connection.close();
  }
}

module.exports = {
  connectToMongoose,
  saveToMongoDB
};
