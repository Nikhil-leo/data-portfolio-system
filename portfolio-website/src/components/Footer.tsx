import { BarChart2 } from "lucide-react";
import profile from "@/data/profile.json";

export default function Footer() {
  return (
    <footer className="py-8 border-t border-slate-800">
      <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-slate-500 text-sm">
          <BarChart2 size={16} className="text-blue-400" />
          <span className="gradient-text font-semibold">{profile.name}</span>
          <span>· Data Analyst Portfolio</span>
        </div>
        <p className="text-slate-600 text-sm">
          © {new Date().getFullYear()} · Built with Next.js &amp; Tailwind CSS
        </p>
      </div>
    </footer>
  );
}
