import { useState } from "react";
import Header from "./components/Header";
import UploadExcel from "./components/UploadExcel";
import EmployeeList from "./components/EmployeeList";
import PayslipActions from "./components/PayslipActions";

export default function App() {
  const [employees, setEmployees] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);

  const handleUploadSuccess = (data) => {
    setEmployees(data);
    setSelectedIds([]);
  };

  const handleSelectEmployee = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((e) => e !== id) : [...prev, id],
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-purple-50 to-indigo-100">
      <Header />

      <UploadExcel onUploadSuccess={handleUploadSuccess} />

      {employees.length > 0 && (
        <>
          <EmployeeList
            employees={employees}
            onSelectEmployee={handleSelectEmployee}
            selectedIds={selectedIds}
          />
          <PayslipActions employees={employees} selectedIds={selectedIds} />
        </>
      )}

      {/* Footer */}
      <div className="text-center py-6 text-gray-400 text-sm">
        Built with ⚡ FastAPI + React — PayrollPro 2026
      </div>
    </div>
  );
}
