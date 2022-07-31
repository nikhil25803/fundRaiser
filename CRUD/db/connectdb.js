const mongoose =require('mongoose');

const connectDB = async (DATABASE_URL) => {
    try {
        const DB_OPTIONS = {
            dbName: 'school',
        }
        await mongoose.connect(DATABASE_URL, DB_OPTIONS);
        console.log('Connected Successfully');
    } catch (err) {
        console.log(err);
    }
}

module.exports = connectDB;