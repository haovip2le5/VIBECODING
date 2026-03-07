import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [students, setStudents] = useState([]);
  const [editingStudent, setEditingStudent] = useState(null);
  const [formData, setFormData] = useState({
    student_id: '',
    name: '',
    birth_year: '',
    major: '',
    gpa: ''
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    const response = await axios.get('http://localhost:8000/students');
    setStudents(response.data);
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingStudent) {
      await axios.put(`http://localhost:8000/students/${editingStudent.student_id}`, formData);
      setEditingStudent(null);
    } else {
      await axios.post('http://localhost:8000/students', formData);
    }
    setFormData({ student_id: '', name: '', birth_year: '', major: '', gpa: '' });
    fetchStudents();
  };

  const handleEdit = (student) => {
    setEditingStudent(student);
    setFormData(student);
  };

  const handleDelete = async (student_id) => {
    await axios.delete(`http://localhost:8000/students/${student_id}`);
    fetchStudents();
  };

  return (
    <div className="App">
      <h1>Student Management System</h1>
      <div className="container">
        <div className="student-list">
          <h2>Student List</h2>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Major</th>
                <th>GPA</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.student_id}>
                  <td>{student.student_id}</td>
                  <td>{student.name}</td>
                  <td>{student.major}</td>
                  <td>{student.gpa}</td>
                  <td>
                    <button onClick={() => handleEdit(student)}>Edit</button>
                    <button onClick={() => handleDelete(student.student_id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="add-student">
          <h2>{editingStudent ? 'Edit Student' : 'Add Student'}</h2>
          <form onSubmit={handleSubmit}>
            <input type="text" name="student_id" placeholder="Student ID" value={formData.student_id} onChange={handleInputChange} required />
            <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleInputChange} required />
            <input type="number" name="birth_year" placeholder="Birth Year" value={formData.birth_year} onChange={handleInputChange} required />
            <input type="text" name="major" placeholder="Major" value={formData.major} onChange={handleInputChange} required />
            <input type="number" step="0.01" name="gpa" placeholder="GPA" value={formData.gpa} onChange={handleInputChange} required />
            <button type="submit">{editingStudent ? 'Update Student' : 'Add Student'}</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;