export default function EmployeeList({
  employees,
  onSelectEmployee,
  selectedIds,
}) {
  const levelColors = {
    Intern: "bg-green-100 text-green-700",
    Junior: "bg-blue-100 text-blue-700",
    Senior: "bg-orange-100 text-orange-700",
    Manager: "bg-purple-100 text-purple-700",
  };

  return (
    <div className="max-w-6xl mx-auto m-6">
      <div className="bg-white rounded-2xl shadow-lg p-8">
        {/* Step Label */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <span className="bg-violet-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm">
              2
            </span>
            <h2 className="text-xl font-bold text-gray-700">
              Select Employee(s)
            </h2>
          </div>
          <span className="text-sm text-gray-400">
            {selectedIds.length} of {employees.length} selected
          </span>
        </div>

        {/* Stats Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {["Intern", "Junior", "Senior", "Manager"].map((level) => {
            const count = employees.filter((e) => e.level === level).length;
            return (
              <div
                key={level}
                className={`rounded-xl p-3 text-center ${levelColors[level]}`}
              >
                <p className="text-2xl font-bold">{count}</p>
                <p className="text-xs font-medium">{level}s</p>
              </div>
            );
          })}
        </div>

        {/* Employee Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {employees.map((emp) => (
            <div
              key={emp.employee_id}
              onClick={() => onSelectEmployee(emp.employee_id)}
              className={`border-2 rounded-2xl p-5 cursor-pointer transition-all duration-200 hover:shadow-md hover:-translate-y-1 ${
                selectedIds.includes(emp.employee_id)
                  ? "border-violet-500 bg-violet-50 shadow-md"
                  : "border-gray-100 hover:border-violet-300"
              }`}
            >
              {/* Top Row */}
              <div className="flex justify-between items-start mb-3">
                <div className="bg-gradient-to-br from-violet-500 to-indigo-500 text-white w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm">
                  {emp.name.charAt(0)}
                </div>
                <span
                  className={`text-xs px-2 py-1 rounded-full font-medium ${levelColors[emp.level]}`}
                >
                  {emp.level}
                </span>
              </div>

              {/* Employee Info */}
              <h3 className="font-bold text-gray-800">{emp.name}</h3>
              <p className="text-sm text-gray-500">{emp.designation}</p>
              <p className="text-xs text-gray-400 mt-1">{emp.department}</p>

              {/* Bottom Row */}
              <div className="mt-3 flex justify-between items-center">
                <p className="text-xs text-gray-400">ID: {emp.employee_id}</p>
                <p className="text-sm font-bold text-green-600">
                  Rs. {emp.basic_salary.toLocaleString()}
                </p>
              </div>

              {selectedIds.includes(emp.employee_id) && (
                <div className="mt-3 text-xs text-violet-600 font-semibold flex items-center gap-1">
                  ✓ Selected for payslip
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
