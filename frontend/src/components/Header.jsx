export default function Header() {
  return (
    <div className="bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 text-white py-6 px-6 shadow-lg">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">
            💼 PayrollPro
          </h1>
          <p className="text-purple-200 text-sm mt-1">
            Upload Excel → Calculate Salary → Generate PDF Payslips
          </p>
        </div>
        <div className="hidden md:flex gap-3">
          <span className="bg-purple-800 text-purple-100 px-4 py-2 rounded-full text-sm font-medium">
            🚀 Automated
          </span>
          <span className="bg-purple-800 text-purple-100 px-4 py-2 rounded-full text-sm font-medium">
            📄 PDF Ready
          </span>
        </div>
      </div>
    </div>
  );
}
