const express = require('express');
const StudentModel = require('../models/student');

class StudentController {
    static createDoc = async (req, res) => {
        try {
            const { name, age, fees } = req.body
            const doc = new StudentModel({
                name: name,
                age: age,
                fees: fees
            })
            const result = await doc.save()
            res.send(result)
        } catch (error) {
            console.log(error);
        }
    }
    static getAllDoc = async (req, res) => {
        // res.send('All Data');
        try {
            const result = await StudentModel.find();
            res.send(result)
        } catch (error) {
            console.log(error)
        }
    }
    static getSingleDocById = async (req, res) => {
        try {
            const result = await StudentModel.findById(req.params.id);
            res.send(result)
        } catch (error) {
            console.log(error)
        }
    }
    static updateSingleDocById = (req, res) => {
        res.send('Update data by Id');
    }
    static deleteSingleDocById = (req, res) => {
        res.send('Delete data by Id');
    }
}

module.exports = StudentController;