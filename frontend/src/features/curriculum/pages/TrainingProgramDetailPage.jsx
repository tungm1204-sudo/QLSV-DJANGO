import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus, LayoutList } from 'lucide-react';
import { useTrainingProgramDetail } from '../hooks/useTrainingPrograms';
import { useKnowledgeBlocks, useKnowledgeBlockMutations } from '../hooks/useCurriculumDetails';
import { usePermissions } from '@/hooks/usePermissions';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import ConfirmModal from '@/components/ui/ConfirmModal';
import KnowledgeBlockList from '../components/KnowledgeBlockList';
import KnowledgeBlockFormModal from '../components/KnowledgeBlockFormModal';

export default function TrainingProgramDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { hasPermission } = usePermissions();
  
  const { data: program, isLoading: isProgramLoading } = useTrainingProgramDetail(id);
  const { data: blocks = [], isLoading: isBlocksLoading } = useKnowledgeBlocks({ training_program: id });

  const [isBlockFormOpen, setIsBlockFormOpen] = useState(false);
  const [selectedBlock, setSelectedBlock] = useState(null);
  const [deleteBlockConfig, setDeleteBlockConfig] = useState({ isOpen: false, id: null });

  const { createMutation, updateMutation, deleteMutation } = useKnowledgeBlockMutations(() => {
    setIsBlockFormOpen(false);
    setSelectedBlock(null);
    setDeleteBlockConfig({ isOpen: false, id: null });
  });

  const handleOpenBlockForm = (block = null) => {
    setSelectedBlock(block);
    setIsBlockFormOpen(true);
  };

  const handleSubmitBlockForm = (formData) => {
    if (selectedBlock) {
      updateMutation.mutate({ id: selectedBlock.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDeleteBlock = () => {
    if (deleteBlockConfig.id) {
      deleteMutation.mutate(deleteBlockConfig.id);
    }
  };

  if (isProgramLoading) {
    return <div className="p-8 max-w-7xl mx-auto"><Skeleton className="h-32 w-full" /></div>;
  }

  if (!program) {
    return <div className="p-8 text-center text-slate-500">Không tìm thấy Chương trình đào tạo</div>;
  }

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-4 mb-2">
        <Button variant="ghost" size="icon" onClick={() => navigate('/curriculum/training-programs')} className="h-8 w-8 hover:bg-slate-200 shrink-0">
          <ArrowLeft className="w-5 h-5 text-slate-700" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-slate-900 leading-tight">
            Cấu hình CTĐT: {program.name}
          </h1>
          <div className="flex gap-3 text-sm text-slate-600 mt-1 font-medium">
            <span>Mã: {program.code}</span>
            <span>•</span>
            <span>Khóa: {program.cohort?.code || 'N/A'}</span>
            <span>•</span>
            <span>Yêu cầu: {program.total_credits} TC</span>
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div className="flex items-center gap-2">
          <LayoutList className="w-5 h-5 text-indigo-600" />
          <h2 className="text-lg font-semibold text-slate-800">Cấu trúc Khối kiến thức</h2>
        </div>
        {hasPermission('curriculum.change_trainingprogram') && (
          <Button onClick={() => handleOpenBlockForm()} className="bg-indigo-600 hover:bg-indigo-700">
            <Plus className="w-4 h-4 mr-2" /> Thêm Khối
          </Button>
        )}
      </div>

      <div className="space-y-4">
        {isBlocksLoading ? (
          <Skeleton className="h-64 w-full rounded-xl" />
        ) : blocks.length === 0 ? (
          <div className="bg-white border border-slate-200 rounded-xl p-12 text-center text-slate-500 shadow-sm">
            Chưa có khối kiến thức nào được thiết lập.
          </div>
        ) : (
          blocks.map(block => (
            <KnowledgeBlockList
              key={block.id}
              block={block}
              trainingProgramId={program.id}
              canUpdate={hasPermission('curriculum.change_trainingprogram')}
              canDelete={hasPermission('curriculum.change_trainingprogram')}
              onEditBlock={handleOpenBlockForm}
              setDeleteBlockConfig={setDeleteBlockConfig}
            />
          ))
        )}
      </div>

      <KnowledgeBlockFormModal
        isOpen={isBlockFormOpen}
        onClose={() => setIsBlockFormOpen(false)}
        initialData={selectedBlock}
        trainingProgramId={program.id}
        onSubmit={handleSubmitBlockForm}
        isLoading={createMutation.isLoading || updateMutation.isLoading}
      />

      <ConfirmModal
        isOpen={deleteBlockConfig.isOpen}
        onClose={() => setDeleteBlockConfig({ isOpen: false, id: null })}
        onConfirm={handleDeleteBlock}
        title="Xóa khối kiến thức"
        description="Bạn có chắc chắn muốn xóa khối kiến thức này? Hành động này sẽ xóa kèm toàn bộ danh sách môn học bên trong khối."
        isLoading={deleteMutation.isLoading}
      />
    </div>
  );
}
