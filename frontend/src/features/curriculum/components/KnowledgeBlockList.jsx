import { Edit2, Trash2, Plus, BookOpen, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Skeleton } from '@/components/ui/skeleton';
import { useTrainingProgramCourses, useTrainingProgramCourseMutations } from '../hooks/useCurriculumDetails';
import { useState } from 'react';
import ConfirmModal from '@/components/ui/ConfirmModal';
import TrainingProgramCourseFormModal from './TrainingProgramCourseFormModal';

export default function KnowledgeBlockList({
  block,
  trainingProgramId,
  canUpdate,
  canDelete,
  onEditBlock,
  setDeleteBlockConfig
}) {
  const { data: courses = [], isLoading } = useTrainingProgramCourses({ 
    training_program: trainingProgramId,
    knowledge_block: block.id
  });

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });

  const { createMutation, updateMutation, deleteMutation } = useTrainingProgramCourseMutations(() => {
    setIsFormOpen(false);
    setSelectedCourse(null);
    setDeleteConfig({ isOpen: false, id: null });
  });

  const handleOpenForm = (course = null) => {
    setSelectedCourse(course);
    setIsFormOpen(true);
  };

  const handleSubmitForm = (formData) => {
    if (selectedCourse) {
      updateMutation.mutate({ id: selectedCourse.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDelete = () => {
    if (deleteConfig.id) {
      deleteMutation.mutate(deleteConfig.id);
    }
  };

  const totalMandatory = courses.filter(c => c.is_mandatory).reduce((sum, c) => sum + (c.course?.credits || 0), 0);
  const totalElective = courses.filter(c => !c.is_mandatory).reduce((sum, c) => sum + (c.course?.credits || 0), 0);

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm mb-6 overflow-hidden">
      <div className="bg-slate-50 px-5 py-4 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h3 className="text-lg font-bold text-slate-800">
            {block.order}. {block.name} <span className="text-sm font-medium text-slate-500 ml-2">({block.code})</span>
          </h3>
          <div className="flex items-center gap-4 mt-2 text-sm text-slate-600">
            <span className={totalMandatory < block.mandatory_credits ? 'text-red-600 font-medium' : 'text-emerald-600 font-medium'}>
              Bắt buộc: {totalMandatory} / {block.mandatory_credits} TC
            </span>
            <span className={totalElective < block.elective_credits ? 'text-amber-600 font-medium' : 'text-emerald-600 font-medium'}>
              Tự chọn: {totalElective} / {block.elective_credits} TC
            </span>
          </div>
          {block.notes && <p className="text-sm text-slate-500 mt-1 italic">{block.notes}</p>}
        </div>
        
        <div className="flex gap-2">
          {canUpdate && (
            <Button size="sm" variant="outline" onClick={() => handleOpenForm()} className="bg-white">
              <Plus className="w-4 h-4 mr-2" /> Thêm Học phần
            </Button>
          )}
          {canUpdate && (
            <Button size="icon" variant="ghost" className="h-9 w-9 text-indigo-600 hover:bg-indigo-50" onClick={() => onEditBlock(block)} title="Sửa thông tin Khối">
              <Settings className="w-4 h-4" />
            </Button>
          )}
          {canDelete && (
            <Button size="icon" variant="ghost" className="h-9 w-9 text-red-600 hover:bg-red-50" onClick={() => setDeleteBlockConfig({ isOpen: true, id: block.id })} title="Xóa Khối">
              <Trash2 className="w-4 h-4" />
            </Button>
          )}
        </div>
      </div>

      <div className="overflow-x-auto">
        <Table className="text-sm min-w-[700px]">
          <TableHeader>
            <TableRow>
              <TableHead className="w-[10%]">Học kỳ</TableHead>
              <TableHead className="w-[15%]">Mã MH</TableHead>
              <TableHead className="w-[30%]">Tên Học phần</TableHead>
              <TableHead className="text-center w-[10%]">Tín chỉ</TableHead>
              <TableHead className="w-[15%]">Loại</TableHead>
              <TableHead className="text-right w-[15%]">Hành động</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              Array.from({ length: 2 }).map((_, idx) => (
                <TableRow key={idx}>
                  <TableCell><Skeleton className="w-10 h-4" /></TableCell>
                  <TableCell><Skeleton className="w-16 h-4" /></TableCell>
                  <TableCell><Skeleton className="w-32 h-4" /></TableCell>
                  <TableCell className="text-center"><Skeleton className="w-6 h-4 mx-auto" /></TableCell>
                  <TableCell><Skeleton className="w-20 h-4" /></TableCell>
                  <TableCell className="text-right"><Skeleton className="w-16 h-8 rounded ml-auto" /></TableCell>
                </TableRow>
              ))
            ) : courses.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-8 text-slate-500">
                  Chưa có học phần nào trong khối kiến thức này
                </TableCell>
              </TableRow>
            ) : (
              courses.map(tpc => (
                <TableRow key={tpc.id} className="hover:bg-slate-50/50">
                  <TableCell className="font-medium text-center">HK {tpc.semester_expected}</TableCell>
                  <TableCell className="font-medium text-slate-700">{tpc.course?.code}</TableCell>
                  <TableCell className="font-semibold text-slate-900">{tpc.course?.name}</TableCell>
                  <TableCell className="text-center font-medium">{tpc.course?.credits}</TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-md text-xs font-medium ${tpc.is_mandatory ? 'bg-rose-100 text-rose-700' : 'bg-blue-100 text-blue-700'}`}>
                      {tpc.is_mandatory ? 'Bắt buộc' : 'Tự chọn'}
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-1">
                      <Button
                        variant="ghost" size="icon" className="h-8 w-8 hover:bg-indigo-50"
                        disabled={!canUpdate} onClick={() => handleOpenForm(tpc)} title="Sửa học phần"
                      >
                        <Edit2 className="h-4 w-4 text-indigo-600" />
                      </Button>
                      <Button
                        variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50"
                        disabled={!canDelete} onClick={() => setDeleteConfig({ isOpen: true, id: tpc.id })} title="Gỡ học phần"
                      >
                        <Trash2 className="h-4 w-4 text-red-600" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <TrainingProgramCourseFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        initialData={selectedCourse}
        trainingProgramId={trainingProgramId}
        knowledgeBlockId={block.id}
        onSubmit={handleSubmitForm}
        isLoading={createMutation.isLoading || updateMutation.isLoading}
      />

      <ConfirmModal
        isOpen={deleteConfig.isOpen}
        onClose={() => setDeleteConfig({ isOpen: false, id: null })}
        onConfirm={handleDelete}
        title="Gỡ học phần"
        description={`Bạn có chắc chắn muốn gỡ bỏ học phần này khỏi khối ${block.name}?`}
        isLoading={deleteMutation.isLoading}
      />
    </div>
  );
}
