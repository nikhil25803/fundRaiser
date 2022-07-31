
const mongoose = require('mongoose');


const studentSchema = new mongoose.Schema({
    name: { type: String, required: true, trim: true },
    age: { type: Number, required: true },
    fees: { type: Number, required: true, validate: (value) => value >= 5000 },
});


// Model

const StudentModel = mongoose.model("student", studentSchema);

module.exports = StudentModel;