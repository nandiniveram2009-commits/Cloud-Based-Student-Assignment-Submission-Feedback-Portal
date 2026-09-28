import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function StudentDashboard() {
  const [assignments, setAssignments] = useState([]);
  const [submissions, setSubmissions] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [activeAssignmentId, setActiveAssignmentId] = useState(null);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const studentName = localStorage.getItem('name') || 'Student';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const assignRes = await API.get('/assignments');
      setAssignments(assignRes.data);
      const subRes = await API.get('/submissions/me');
      setSubmissions(subRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpload = async (assignmentId) => {
    if (!selectedFile) {
      alert('Please select a file to upload.');
      return;
    }
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await API.post(`/assignments/${assignmentId}/submit`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMessage('Assignment submitted successfully!');
      setSelectedFile(null);
      fetchData();
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Upload failed.');
    }
  };

  const logout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8 bg-white p-6 rounded-xl shadow">
          <div>
            <h1 className="text-3xl font-bold text-slate-800">Welcome, {studentName}</h1>
            <p className="text-slate-500">Student Assignment Submission Portal</p>
          </div>
          <button onClick={logout} className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">Logout</button>
        </div>

        {message && <div className="mb-6 p-4 bg-blue-100 text-blue-800 rounded-lg">{message}</div>}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-xl shadow">
            <h2 className="text-xl font-bold mb-4 text-slate-800">Available Assignments</h2>
            <div className="space-y-4">
              {assignments.map((assign) => (
                <div key={assign.assignment_id} className="p-4 border rounded-lg bg-slate-50">
                  <h3 className="font-semibold text-lg text-slate-800">{assign.title}</h3>
                  <p className="text-sm text-slate-600 mb-2">{assign.description}</p>
                  <p className="text-xs text-red-600 font-medium mb-3">Deadline: {new Date(assign.deadline).toLocaleString()}</p>
                  <div className="flex items-center space-x-2">
                    <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} className="text-sm" />
                    <button onClick={() => handleUpload(assign.assignment_id)} className="px-4 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">Submit</button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow">
            <h2 className="text-xl font-bold mb-4 text-slate-800">My Submissions & Feedback</h2>
            <div className="space-y-4">
              {submissions.map((sub) => (
                <div key={sub.submission_id} className="p-4 border rounded-lg bg-slate-50">
                  <p className="font-semibold text-slate-800">Assignment ID: {sub.assignment_id}</p>
                  <p className="text-sm text-slate-600">File: {sub.file_name}</p>
                  <p className="text-xs font-semibold mt-1">Status: <span className="text-emerald-600">{sub.submission_status}</span></p>
                  <p className="text-sm text-blue-600 mt-1">Marks: {sub.marks !== null ? `${sub.marks}` : 'Pending'}</p>
                  <p className="text-sm text-slate-700 mt-1 italic">Feedback: {sub.feedback || 'No feedback yet.'}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
                }
