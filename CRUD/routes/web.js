const express = require('express');
const router = express.Router();
const StudentController = require('../controllers/studentController');


router.get('/', StudentController.getAllDoc);
router.post('/', StudentController.createDoc);
router.get('/:id', StudentController.getSingleDocById);
router.put('/:id', StudentController.updateSingleDocById);
router.delete('/:id', StudentController.deleteSingleDocById);

// export default router;
module.exports = router;