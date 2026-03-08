import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [students, setStudents] = useState([]);
  const [classes, setClasses] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [editingStudent, setEditingStudent] = useState(null);
  const [searchName, setSearchName] = useState('');
  const [formData, setFormData] = useState({
    student_id: '',
    name: '',
    birth_year: '',
    major: '',
    gpa: '',
    class_id: ''
  });

  useEffect(() => {
    fetchStudents();
    fetchClasses();
    fetchStatistics();
  }, []);

  const fetchStudents = async (name = '') => {
    const response = await axios.get(`http://localhost:8000/students?name=${name}`);
    setStudents(response.data);
  };

  const fetchClasses = async () => {
    try {
      const response = await axios.get('http://localhost:8000/classes');
      setClasses(response.data);
    } catch (error) {
      console.log('Classes not available yet');
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await axios.get('http://localhost:8000/statistics');
      setStatistics(response.data);
    } catch (error) {
      console.log('Statistics not available yet');
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSearchChange = (e) => {
    setSearchName(e.target.value);
  };

  const handleSearch = () => {
    fetchStudents(searchName);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingStudent) {
      await axios.put(`http://localhost:8000/students/${editingStudent.student_id}`, formData);
      setEditingStudent(null);
    } else {
      await axios.post('http://localhost:8000/students', formData);
    }
    setFormData({ student_id: '', name: '', birth_year: '', major: '', gpa: '', class_id: '' });
    fetchStudents();
    fetchStatistics();
  };

  const handleEdit = (student) => {
    setEditingStudent(student);
    setFormData(student);
  };

  const handleDelete = async (student_id) => {
    if (window.confirm('Are you sure?')) {
      await axios.delete(`http://localhost:8000/students/${student_id}`);
      fetchStudents();
      fetchStatistics();
    }
  };

  const handleExport = async () => {
    try {
      const response = await axios.get('http://localhost:8000/export/csv');
      const blob = new Blob([response.data.csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'students.csv';
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert('Export failed');
    }
  };

  return (
    <div className="App">
      <h1>Student Management System</h1>
      
      <div className="search-section">
        <input 
          type="text" 
          placeholder="Search by name" 
          value={searchName} 
          onChange={handleSearchChange} 
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <div className="statistics-section">
        <h3>Statistics</h3>
        <p>Total Students: <strong>{statistics.total_students}</strong></p>
        <p>Average GPA: <strong>{statistics.average_gpa}</strong></p>
        {statistics.students_by_major && (
          <p>Students by Major: <strong>
            {Object.entries(statistics.students_by_major || {}).map(([major, count]) => `${major}: ${count}`).join(', ')}
          </strong></p>
        )}
        <button onClick={handleExport} className="export-btn">Export to CSV</button>
      </div>

      <div className="container">
        <div className="student-list">
          <h2>Student List</h2>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Birth Year</th>
                <th>Major</th>
                <th>GPA</th>
                <th>Class</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {students.map(student => (
                <tr key={student.student_id}>
                  <td>{student.student_id}</td>
                  <td>{student.name}</td>
                  <td>{student.birth_year}</td>
                  <td>{student.major}</td>
                  <td>{student.gpa}</td>
                  <td>{student.class_name || 'N/A'}</td>
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
            <input 
              type="text" 
              name="student_id" 
              placeholder="Student ID" 
              value={formData.student_id} 
              onChange={handleInputChange} 
              disabled={editingStudent} 
              required 
            />
            <input 
              type="text" 
              name="name" 
              placeholder="Name" 
              value={formData.name} 
              onChange={handleInputChange} 
              required 
            />
            <input 
              type="number" 
              name="birth_year" 
              placeholder="Birth Year" 
              value={formData.birth_year} 
              onChange={handleInputChange} 
              required 
            />
            <input 
              type="text" 
              name="major" 
              placeholder="Major" 
              value={formData.major} 
              onChange={handleInputChange} 
              required 
            />
            <input 
              type="number" 
              step="0.01" 
              name="gpa" 
              placeholder="GPA" 
              value={formData.gpa} 
              onChange={handleInputChange} 
              required 
            />
            <select 
              name="class_id" 
              value={formData.class_id} 
              onChange={handleInputChange}
            >
              <option value="">Select Class (Optional)</option>
              {classes.map(cls => (
                <option key={cls.class_id} value={cls.class_id}>
                  {cls.class_name} ({cls.class_id})
                </option>
              ))}
            </select>
            <button type="submit">{editingStudent ? 'Update Student' : 'Add Student'}</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;