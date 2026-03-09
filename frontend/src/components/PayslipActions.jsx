import { useState } from "react";
import axios from "axios";

const API = "https://payroll-system-h50d.onrender.com";

export default function PayslipActions({ employees, selectedIds }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const downloadPayslip = async (employeeId) => {
    const res = await axios.get(`${API}/generate-payslip/${employeeId}`, {
      responseType: "blob",
    });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${employeeId}_Payslip.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const handleSelected = async () => {
    try {
      setLoading(true);
      setMessage("");
      setSuccess(false);
      for (const id of selectedIds) {
        await downloadPayslip(id);
      }
      setSuccess(true);
      setMessage(
        `✅ ${selectedIds.length} payslip(s) downloaded successfully!`,
      );
    } catch (err) {
      setMessage("⚠️ Failed to generate payslips. Please try again.");
      setSuccess(false);
    } finally {
      setLoading(false);
    }
  };

  const handleAll = async () => {
    try {
      setLoading(true);
      setMessage("");
      setSuccess(false);
      for (const emp of employees) {
        await downloadPayslip(emp.employee_id);
      }
      setSuccess(true);
      setMessage(
        `✅ All ${employees.length} payslips downloaded successfully!`,
      );
    } catch (err) {
      setMessage("⚠️ Failed to generate payslips. Please try again.");
      setSuccess(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto m-6">
      <div className="bg-white rounded-2xl shadow-lg p-8">
        {/* Step Label */}
        <div className="flex items-center gap-3 mb-6">
          <span className="bg-violet-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">
            3
          </span>
          <h2 className="text-xl font-bold text-gray-700">Generate Payslips</h2>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gradient-to-br from-violet-50 to-indigo-50 border border-violet-100 rounded-2xl p-4 text-center">
            <p className="text-3xl font-extrabold text-violet-600">
              {employees.length}
            </p>
            <p className="text-sm text-gray-500 mt-1">Total Employees</p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-100 rounded-2xl p-4 text-center">
            <p className="text-3xl font-extrabold text-green-600">
              {selectedIds.length}
            </p>
            <p className="text-sm text-gray-500 mt-1">Selected</p>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex gap-4 flex-wrap">
          <button
            onClick={handleSelected}
            disabled={loading || selectedIds.length === 0}
            className="flex items-center gap-2 bg-gradient-to-r from-violet-600 to-indigo-600 text-white px-6 py-3 rounded-xl font-semibold hover:opacity-90 disabled:opacity-40 transition-all duration-200 shadow-md"
          >
            📥 Download Selected ({selectedIds.length})
          </button>

          <button
            onClick={handleAll}
            disabled={loading || employees.length === 0}
            className="flex items-center gap-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-3 rounded-xl font-semibold hover:opacity-90 disabled:opacity-40 transition-all duration-200 shadow-md"
          >
            📦 Download All Payslips
          </button>
        </div>

        {/* Message */}
        {message && (
          <div
            className={`mt-4 p-4 rounded-xl text-sm font-medium ${
              success
                ? "bg-green-50 text-green-700 border border-green-200"
                : "bg-red-50 text-red-700 border border-red-200"
            }`}
          >
            {message}
          </div>
        )}
      </div>
    </div>
  );
}
