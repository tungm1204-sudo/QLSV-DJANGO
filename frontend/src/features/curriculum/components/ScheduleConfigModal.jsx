import { useEffect, useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { AlertCircle, Plus, Edit, Trash2, CalendarDays } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { zodResolver } from '@hookform/resolvers/zod';
import { scheduleSchema } from '../validations/scheduleSchema';
import { useRoomOptions } from '../../master_data/hooks/useMasterDataOptions';
import { useSchedules, useScheduleMutations } from '../hooks/useSchedules';
import ConfirmModal from '@/components/ui/ConfirmModal';

export default function ScheduleConfigModal({ 
  isOpen, 
  onClose, 
  offering = null 
}) {
  const { data: roomsData } = useRoomOptions();
  const rooms = roomsData || [];

  const [selectedSchedule, setSelectedSchedule] = useState(null);
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });
  const [conflicts, setConflicts] = useState([]);
  
  // Fetch existing schedules for this offering
  const { data: schedulesData, isLoading: isSchedulesLoading } = useSchedules(
    { course_offering_id: offering?.id },
    { enabled: !!offering?.id && isOpen }
  );
  const schedules = schedulesData?.results || [];

  const { createMutation, updateMutation, deleteMutation, validateMutation } = useScheduleMutations(() => {
    resetForm();
  });

  const { register, handleSubmit, reset, control, formState: { errors } } = useForm({
    resolver: zodResolver(scheduleSchema),
    defaultValues: {
      room: '',
      day_of_week: 2,
      start_period: 1,
      end_period: 3,
    }
  });

  useEffect(() => {
    if (selectedSchedule) {
      reset({
        room: selectedSchedule.room?.id || selectedSchedule.room,
        day_of_week: selectedSchedule.day_of_week,
        start_period: selectedSchedule.start_period,
        end_period: selectedSchedule.end_period,
      });
      setConflicts([]);
    } else {
      resetForm();
    }
  }, [selectedSchedule, reset]);
  
  const resetForm = () => {
    reset({
      room: '',
      day_of_week: 2,
      start_period: 1,
      end_period: 3,
    });
    setSelectedSchedule(null);
    setConflicts([]);
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const onSubmit = async (data) => {
    setConflicts([]);
    const payload = {
      ...data,
      course_offering: offering?.id,
    };
    if (selectedSchedule) {
      payload.exclude_schedule_id = selectedSchedule.id;
    }

    try {
      // 1. Call Validate API first
      const res = await validateMutation.mutateAsync(payload);
      
      // 2. If valid, proceed to save
      if (res.data?.valid) {
        if (selectedSchedule) {
          updateMutation.mutate({ id: selectedSchedule.id, data: payload });
        } else {
          createMutation.mutate(payload);
        }
      } else {
        // 3. Render conflicts
        setConflicts(res.data?.conflicts || []);
      }
    } catch (err) {
      // Handled globally by the hook if it's a hard error
      console.error(err);
    }
  };

  const handleDelete = () => {
    if (deleteConfig.id) {
      deleteMutation.mutate(deleteConfig.id, {
        onSuccess: () => setDeleteConfig({ isOpen: false, id: null })
      });
    }
  };

  const isSaving = createMutation.isLoading || updateMutation.isLoading || validateMutation.isLoading;

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && handleClose()}>
      <DialogContent className="sm:max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <CalendarDays className="w-5 h-5 text-indigo-600" />
            Xếp lịch học phần: <span className="font-bold">{offering?.course?.name} ({offering?.course?.code})</span>
          </DialogTitle>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
          {/* Cột trái: Form xếp lịch */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <h3 className="font-semibold text-slate-700 mb-4">
              {selectedSchedule ? 'Sửa lịch' : 'Thêm lịch mới'}
            </h3>
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="space-y-2">
                <Label>Phòng học <span className="text-red-500">*</span></Label>
                <Controller
                  name="room"
                  control={control}
                  render={({ field }) => (
                    <Select onValueChange={field.onChange} value={field.value || ""}>
                      <SelectTrigger>
                        <SelectValue placeholder="Chọn phòng" />
                      </SelectTrigger>
                      <SelectContent>
                        {rooms.map((r) => (
                          <SelectItem key={r.id} value={r.id}>{r.name} - {r.building?.name}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
                {errors.room && <p className="text-sm text-red-500">{errors.room.message}</p>}
              </div>

              <div className="space-y-2">
                <Label>Thứ <span className="text-red-500">*</span></Label>
                <Controller
                  name="day_of_week"
                  control={control}
                  render={({ field }) => (
                    <Select onValueChange={(v) => field.onChange(parseInt(v))} value={field.value ? field.value.toString() : ""}>
                      <SelectTrigger>
                        <SelectValue placeholder="Chọn thứ" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="2">Thứ 2</SelectItem>
                        <SelectItem value="3">Thứ 3</SelectItem>
                        <SelectItem value="4">Thứ 4</SelectItem>
                        <SelectItem value="5">Thứ 5</SelectItem>
                        <SelectItem value="6">Thứ 6</SelectItem>
                        <SelectItem value="7">Thứ 7</SelectItem>
                        <SelectItem value="8">Chủ nhật</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                />
                {errors.day_of_week && <p className="text-sm text-red-500">{errors.day_of_week.message}</p>}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Tiết bắt đầu</Label>
                  <Input type="number" min={1} max={15} {...register('start_period', { valueAsNumber: true })} />
                  {errors.start_period && <p className="text-sm text-red-500">{errors.start_period.message}</p>}
                </div>
                <div className="space-y-2">
                  <Label>Tiết kết thúc</Label>
                  <Input type="number" min={1} max={15} {...register('end_period', { valueAsNumber: true })} />
                  {errors.end_period && <p className="text-sm text-red-500">{errors.end_period.message}</p>}
                </div>
              </div>

              {/* Box hiển thị lỗi trùng lịch */}
              {conflicts.length > 0 && (
                <Alert variant="destructive" className="mt-4">
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>Phát hiện trùng lịch!</AlertTitle>
                  <AlertDescription>
                    <ul className="list-disc pl-4 mt-2 space-y-1">
                      {conflicts.map((conflict, idx) => (
                        <li key={idx} className="text-sm">{conflict.message}</li>
                      ))}
                    </ul>
                  </AlertDescription>
                </Alert>
              )}

              <div className="flex gap-2 pt-2">
                {selectedSchedule && (
                  <Button type="button" variant="outline" className="flex-1" onClick={resetForm} disabled={isSaving}>
                    Hủy sửa
                  </Button>
                )}
                <Button type="submit" className={`flex-1 ${selectedSchedule ? 'bg-blue-600 hover:bg-blue-700' : 'bg-indigo-600 hover:bg-indigo-700'}`} disabled={isSaving}>
                  {isSaving ? 'Đang kiểm tra...' : (selectedSchedule ? 'Lưu' : 'Thêm')}
                </Button>
              </div>
            </form>
          </div>

          {/* Cột phải: Danh sách lịch đã xếp */}
          <div className="border border-slate-200 rounded-xl overflow-hidden flex flex-col">
            <div className="bg-slate-100 p-3 border-b border-slate-200">
              <h3 className="font-semibold text-slate-700">Lịch đã xếp</h3>
            </div>
            <div className="p-4 flex-1 overflow-y-auto">
              {isSchedulesLoading ? (
                <div className="text-center text-slate-500 py-4">Đang tải...</div>
              ) : schedules.length === 0 ? (
                <div className="text-center text-slate-500 py-8">Chưa có lịch nào</div>
              ) : (
                <div className="space-y-3">
                  {schedules.map((schedule) => (
                    <div 
                      key={schedule.id} 
                      className={`p-3 border rounded-lg flex items-center justify-between group ${selectedSchedule?.id === schedule.id ? 'border-indigo-500 bg-indigo-50' : 'border-slate-200 bg-white hover:border-indigo-300'}`}
                    >
                      <div>
                        <p className="font-medium text-slate-900">
                          Thứ {schedule.day_of_week === 8 ? 'CN' : schedule.day_of_week} • Tiết {schedule.start_period} - {schedule.end_period}
                        </p>
                        <p className="text-sm text-slate-500">Phòng: {schedule.room?.name}</p>
                      </div>
                      <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setSelectedSchedule(schedule)}>
                          <Edit className="w-4 h-4 text-blue-500" />
                        </Button>
                        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setDeleteConfig({ isOpen: true, id: schedule.id })}>
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </DialogContent>

      <ConfirmModal
        isOpen={deleteConfig.isOpen}
        onClose={() => setDeleteConfig({ isOpen: false, id: null })}
        onConfirm={handleDelete}
        title="Xóa lịch học"
        description="Bạn có chắc chắn muốn xóa lịch học này?"
        isLoading={deleteMutation.isLoading}
      />
    </Dialog>
  );
}
